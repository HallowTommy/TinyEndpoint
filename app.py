"""
app.py

FastAPI application that provides a very small JSON API
for controlling WebView behavior inside a mobile application.

This version keeps the logic intentionally simple:

1. /api/webview-status
   Returns whether WebView should be enabled or disabled.

2. /api/webview-target
   Returns the target URL only when WebView is enabled.

This keeps the application-side logic easy:
- first ask for status
- if enabled, ask for target
- if disabled, do nothing
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from config import (
    webview_power_state,
    upstream_webview_url,
    enabled_status_message,
    disabled_status_message,
)

# Create the FastAPI application instance.
app = FastAPI(
    title="WebView Control API",
    description="Simple JSON API for enabling or disabling WebView and returning the target URL.",
    version="1.0.0",
)


def is_webview_enabled() -> bool:
    """
    Returns True when the WebView flow is enabled in config.py.

    This function reads the power switch from configuration and converts it
    into a boolean value that the rest of the application can use.

    Accepted enabled value:
    - "on"

    Any other value is treated as disabled.
    """
    normalized_power_state = webview_power_state.strip().lower()
    return normalized_power_state == "on"


def build_disabled_response() -> JSONResponse:
    """
    Builds the JSON response used when WebView is disabled.

    Response example:
    {
        "enabled": false,
        "status": "webview_disabled"
    }
    """
    return JSONResponse(
        content={
            "enabled": False,
            "status": disabled_status_message,
        }
    )


def build_enabled_status_response() -> JSONResponse:
    """
    Builds the JSON response used when WebView is enabled.

    Response example:
    {
        "enabled": true,
        "status": "webview_enabled"
    }
    """
    return JSONResponse(
        content={
            "enabled": True,
            "status": enabled_status_message,
        }
    )


def build_enabled_target_response() -> JSONResponse:
    """
    Builds the JSON response containing the WebView target URL.

    This response is only returned when WebView is enabled.

    Response example:
    {
        "enabled": true,
        "status": "webview_enabled",
        "target_url": "https://your-domain.com/index.php"
    }
    """
    return JSONResponse(
        content={
            "enabled": True,
            "status": enabled_status_message,
            "target_url": upstream_webview_url,
        }
    )


@application.get("/")
def root_healthcheck() -> JSONResponse:
    """
    Root endpoint for quick health checks in browser or Postman.

    This is useful to confirm that the FastAPI service is alive.
    """
    return JSONResponse(
        content={
            "service": "webview-control-api",
            "alive": True,
        }
    )


@application.get("/api/webview-status")
def get_webview_status() -> JSONResponse:
    """
    Returns the current WebView power state.

    Use this endpoint first from the mobile application.

    Application logic:
    - if enabled == false -> do not open WebView
    - if enabled == true  -> continue to the next step
    """
    if not is_webview_enabled():
        return build_disabled_response()

    return build_enabled_status_response()


@application.get("/api/webview-target")
def get_webview_target() -> JSONResponse:
    """
    Returns the target URL for WebView only when WebView is enabled.

    Use this endpoint only after /api/webview-status confirms that
    the WebView flow is enabled.

    Application logic:
    - if enabled == false -> stop the flow
    - if enabled == true  -> open WebView with target_url
    """
    if not is_webview_enabled():
        return build_disabled_response()

    return build_enabled_target_response()
