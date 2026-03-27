"""
config.py

Файл конфигурации для управления поведением WebView.

Здесь находятся все настраиваемые параметры.
Можно менять значения, не трогая основную логику приложения.
"""

# Главный переключатель WebView
# Возможные значения:
# - "on"  → WebView включен
# - "off" → WebView выключен
webview_power_state = "off"


# URL, который должен открываться в WebView,
# если WebView разрешен
upstream_webview_url = "https://your-domain.com/"


# Текст статуса, который возвращается приложению,
# когда WebView включен
enabled_status_message = "webview_enabled"


# Текст статуса, который возвращается приложению,
# когда WebView выключен
disabled_status_message = "webview_disabled"


# Таймаут (в секундах) для будущих HTTP-запросов
# (пока не используется)
request_timeout_seconds = 5
