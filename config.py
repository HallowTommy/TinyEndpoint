"""
config.py

Минимальная конфигурация для управления WebView.
Меняешь только эти значения — логика приложения не трогается.
"""

# Главный переключатель WebView
# Возможные значения:
# - "on"  -> WebView включен
# - "off" -> WebView выключен
webview_power_state = "on"

# URL, который должен открываться в WebView,
# если WebView включен
upstream_webview_url = "https://your-domain.com/"
