"""
config.py

This file contains all editable configuration values for the WebView control API.

You can safely change these values without touching the main application logic.
"""

# Master switch for the whole WebView flow.
# Possible values:
# - "on"  -> the API allows the application to continue the WebView flow
# - "off" -> the API disables the WebView flow
webview_power_state = "off"

# The URL that should be opened when WebView is allowed.
# This should be your own upstream URL.
# Example:
# "https://your-domain.com/index.php"
upstream_webview_url = "https://your-domain.com/index.php"

# The public status text returned to the application when WebView is enabled.
enabled_status_message = "webview_enabled"

# The public status text returned to the application when WebView is disabled.
disabled_status_message = "webview_disabled"

# Request timeout (in seconds) for any future upstream checks if you add them later.
request_timeout_seconds = 5
