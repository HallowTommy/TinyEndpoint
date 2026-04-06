# Control API

Небольшой FastAPI-сервис для управления открытием WebView-контента в приложении.

Основная идея:
- приложение обращается к API,
- API решает, можно ли отдавать ссылку для WebView,
- если WebView разрешён — возвращается `target_url`,
- если запрещён или отфильтрован — контейнер остаётся на нативной части / заглушке / white page.

---

## Что делает сервис

Сервис поднимает 3 endpoint'а:

- `GET /` — healthcheck
- `GET /policy` — открывает контент
- `GET /api/webview-target` — основной endpoint для WebView-контейнера

Логика работы такая:

1. Проверяется глобальный флаг `webview_power_state`
2. Если WebView выключен — API сообщает, что WebView отключён
3. Если WebView включён:
   - при `use_hideclick = True` запрос дополнительно прогоняется через HideClick
   - при `use_hideclick = False` ссылка отдаётся сразу
4. Если HideClick разрешил трафик (`action == "allow"`), API возвращает `target_url`
5. Во всех остальных случаях WebView не открывается

---
