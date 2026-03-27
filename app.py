from fastapi import FastAPI
from fastapi.responses import JSONResponse

from config import webview_power_state, upstream_webview_url

app = FastAPI()


def is_webview_enabled() -> bool:
    """
    Проверяет, включен ли WebView.

    Возвращает:
    - True, если webview_power_state == "on"
    - False во всех остальных случаях
    """
    return webview_power_state.strip().lower() == "on"


@app.get("/")
def root_healthcheck() -> JSONResponse:
    """
    Проверка работоспособности API.
    """
    return JSONResponse(
        content={
            "service": "webview-control-api",
            "alive": True,
        }
    )


@app.get("/api/webview-target")
def get_webview_target() -> JSONResponse:
    """
    Возвращает решение для приложения:

    - если WebView выключен -> сообщаем, что он отключен
    - если WebView включен -> сообщаем, что он включен,
      и отдаем target_url для открытия в WebView
    """
    if not is_webview_enabled():
        return JSONResponse(
            content={
                "enabled": False,
                "status": "webview_disabled",
            }
        )

    return JSONResponse(
        content={
            "enabled": True,
            "status": "webview_enabled",
            "target_url": upstream_webview_url,
        }
    )
