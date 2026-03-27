from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

from config import UPSTREAM_URL, REQUEST_TIMEOUT, ALLOWED_BUNDLES, MIN_APP_VERSION

app = FastAPI()


def compare_versions(a: str, b: str) -> int:
    pa = [int(x) for x in a.split(".")]
    pb = [int(x) for x in b.split(".")]
    length = max(len(pa), len(pb))

    for i in range(length):
        va = pa[i] if i < len(pa) else 0
        vb = pb[i] if i < len(pb) else 0
        if va > vb:
            return 1
        if va < vb:
            return -1
    return 0


@app.get("/")
async def root():
    return {"ok": True, "service": "webview-config"}


@app.get("/api/webview-config")
async def webview_config(request: Request):
    bundle_id = request.headers.get("x-app-bundle-id", "")
    app_version = request.headers.get("x-app-version", "")
    user_agent = request.headers.get("user-agent", "AppWebViewCheck/1.0")

    if ALLOWED_BUNDLES and bundle_id not in ALLOWED_BUNDLES:
        return JSONResponse({
            "enabled": False,
            "reason": "bundle_not_allowed"
        })

    if MIN_APP_VERSION and app_version:
        if compare_versions(app_version, MIN_APP_VERSION) < 0:
            return JSONResponse({
                "enabled": False,
                "reason": "version_not_allowed"
            })

    try:
        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT,
            follow_redirects=False
        ) as client:
            resp = await client.get(
                UPSTREAM_URL,
                headers={
                    "User-Agent": user_agent,
                    "Accept": "*/*",
                },
            )

        # 1) Если upstream ответил редиректом — считаем это "включено"
        if resp.status_code in (301, 302, 303, 307, 308):
            location = resp.headers.get("location", "").strip()

            if location.startswith("http://") or location.startswith("https://"):
                return JSONResponse({
                    "enabled": True,
                    "url": UPSTREAM_URL,
                    "reason": "redirect_detected",
                    "target": location,
                    "status_code": resp.status_code
                })

            return JSONResponse({
                "enabled": False,
                "reason": "invalid_redirect_location",
                "status_code": resp.status_code
            })

        # 2) Если пришёл HTML/обычный 200 — считаем "не открывать"
        content_type = resp.headers.get("content-type", "").lower()

        if resp.status_code == 200:
            return JSONResponse({
                "enabled": False,
                "reason": "html_response",
                "status_code": resp.status_code,
                "content_type": content_type
            })

        # 3) Любой другой код — тоже не открывать
        return JSONResponse({
            "enabled": False,
            "reason": "unexpected_status",
            "status_code": resp.status_code,
            "content_type": content_type
        })

    except httpx.TimeoutException:
        return JSONResponse({
            "enabled": False,
            "reason": "timeout"
        })

    except Exception as e:
        return JSONResponse({
            "enabled": False,
            "reason": "request_failed",
            "error": str(e)
        })
