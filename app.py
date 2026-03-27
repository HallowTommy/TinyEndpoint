from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Импортируем настройки из config.py
from config import (
    webview_power_state,
    upstream_webview_url,
    enabled_status_message,
    disabled_status_message,
)

# Создаем FastAPI приложение
app = FastAPI()


def is_webview_enabled() -> bool:
    """
    Проверяет, включен ли WebView.

    Берет значение из config.py и приводит его к нормальному виду:
    - убирает пробелы
    - переводит в нижний регистр

    Возвращает:
    - True  → если включено ("on")
    - False → если выключено
    """
    normalized_power_state = webview_power_state.strip().lower()
    return normalized_power_state == "on"


def build_disabled_response() -> JSONResponse:
    """
    Формирует ответ, когда WebView выключен.
    """
    return JSONResponse(
        content={
            "enabled": False,
            "status": disabled_status_message,
        }
    )


def build_enabled_status_response() -> JSONResponse:
    """
    Формирует ответ, когда WebView включен (без URL).
    """
    return JSONResponse(
        content={
            "enabled": True,
            "status": enabled_status_message,
        }
    )


def build_enabled_target_response() -> JSONResponse:
    """
    Формирует ответ с URL для WebView.
    Используется только когда WebView включен.
    """
    return JSONResponse(
        content={
            "enabled": True,
            "status": enabled_status_message,
            "target_url": upstream_webview_url,
        }
    )


@app.get("/")
def root_healthcheck() -> JSONResponse:
    """
    Проверка, что API работает.

    Можно открыть в браузере:
    /
    """
    return JSONResponse(
        content={
            "service": "webview-control-api",
            "alive": True,
        }
    )


@app.get("/api/webview-status")
def get_webview_status() -> JSONResponse:
    """
    Первый endpoint, который должен дергать плагин.

    Логика:
    - если WebView выключен → возвращаем disabled
    - если включен → возвращаем enabled
    """
    if not is_webview_enabled():
        return build_disabled_response()

    return build_enabled_status_response()


@app.get("/api/webview-target")
def get_webview_target() -> JSONResponse:
    """
    Второй endpoint.

    Дергается только если /api/webview-status вернул enabled.

    Логика:
    - если выключен → стоп
    - если включен → возвращаем URL
    """
    if not is_webview_enabled():
        return build_disabled_response()

    return build_enabled_target_response()
