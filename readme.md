# TinyEndpoint

Сервис для удалённого управления WebView-плагином в мобильном приложении.

---

## Зависимости

Проект использует следующие Python-зависимости:

- `fastapi` — основной фреймворк для создания HTTP API

---

## Конфигурация Vercel

Файл `vercel.json` определяет поведение приложения на Vercel:

- `builds` → указывает точку входа (`app.py`)  
- `routes` → направляет весь входящий трафик в FastAPI  

---

## Структура проекта

### `config.py`

Файл конфигурации.

Отвечает за:
- включение / выключение WebView (основной тумблер)
- URL, который должен открываться в WebView

---

### `app.py`

Основной FastAPI endpoint.

Отвечает за:
- обработку HTTP-запросов
- чтение значений из `config.py`
- формирование JSON-ответов для приложения

Содержит всю серверную логику API.

---

## API

Все запросы выполняются через HTTP GET.

Базовый URL: https://tiny-endpoint.vercel.app


---

### `GET /`

Проверка работоспособности API.

**Ответ:**

```json
{
  "service": "webview-control-api",
  "alive": true
}
```

---

### `GET /api/webview-status`

Возвращает текущее состояние WebView.

**Если WebView выключен (`webview_power_state = "off"`):**

```json
{
  "enabled": false,
  "status": "webview_disabled"
}
```

**Если WebView включен (`webview_power_state = "on"`):**

```json
{
  "enabled": true,
  "status": "webview_enabled"
}
```

---

### `GET /api/webview-target`

Возвращает URL для открытия WebView.

**Если WebView выключен:**

```json
{
  "enabled": false,
  "status": "webview_disabled"
}
```

**Если WebView включен:**

```json
{
  "enabled": true,
  "status": "webview_enabled",
  "target_url": "https://your-domain.com/"
}
```

---
