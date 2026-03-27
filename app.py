from fastapi import FastAPI
from fastapi.responses import JSONResponse

from config import (
    webview_power_state,
    upstream_webview_url,
    enabled_status_message,
    disabled_status_message,
)

app = FastAPI()


def is_webview_enabled() -> bool:
    normalized_power_state = webview_power_state.strip().lower()
    return normalized_power_state == "on"


def build_disabled_response() -> JSONResponse:
    return JSONResponse(
        content={
            "enabled": False,
            "status": disabled_status_message,
        }
    )


def build_enabled_status_response() -> JSONResponse:
    return JSONResponse(
        content={
            "enabled": True,
            "status": enabled_status_message,
        }
    )


def build_enabled_target_response() -> JSONResponse:
    return JSONResponse(
        content={
            "enabled": True,
            "status": enabled_status_message,
            "target_url": upstream_webview_url,
        }
    )


@app.get("/")
def root_healthcheck() -> JSONResponse:
    return JSONResponse(
        content={
            "service": "webview-control-api",
            "alive": True,
        }
    )


@app.get("/api/webview-status")
def get_webview_status() -> JSONResponse:
    if not is_webview_enabled():
        return build_disabled_response()

    return build_enabled_status_response()


@app.get("/api/webview-target")
def get_webview_target() -> JSONResponse:
    if not is_webview_enabled():
        return build_disabled_response()

    return build_enabled_target_response()
