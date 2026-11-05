# Журнал гипотез и векторов (VK MAX)

## 🟢 В работе / Запланировано
- [ ] **Auth API Origin/Referer Bypass**: Проверить `/api/send-code` и `/api/sign-in` на отсутствие проверки заголовков `Origin`/`Referer` (подтверждено статьей на Habr).
- [ ] **IDOR в bot API**: Проверить `GET /self/api/v1/bot` на HPP (`?bot_id=1&bot_id=2`) и подстановку чужих ID.
- [ ] **Mass Assignment**: Внедрение полей `role`, `owner_id`, `verified` в JSON-тело запросов на обновление профиля/организации.
- [ ] **Race Condition**: Поиск эндпоинтов для параллельных запросов (промокоды, создание каналов, отправка сообщений).
- [ ] **HTTP Method Override**: Проверка заголовка `X-HTTP-Method-Override` на критичных эндпоинтах.

## 🔴 Закрыто (Проверено, уязвимости нет)
- [-] **IDOR в `/self/api/v1/organization`**: Параметры `?id=` и `?org_id=` игнорируются, отдаются данные только из сессии.
- [-] **IDOR в `/self/api/v1/organizations`**: Возвращает только организации текущего пользователя.
- [-] **IDOR в `/self/api/v1/permissions`**: Жесткая валидация фильтра, ошибка `wrong filter` при подстановке чужих ID.
- [-] **Open Redirect / XSS в `redirect_uri`**: Сервер возвращает 200 OK (не редиректит), символы экранируются (белый список доменов).
- [-] **IDOR в `/self/api/v1/bot`**: Параметры `?bot_id=1` и HPP (`?bot_id=1&bot_id=2`) возвращают пустой массив `[]` (у аккаунта нет ботов). Прямой IDOR не подтвержден.
- [-] PUT /self/api/v1/organizations: 405 Method Not Allowed (эндпоинт только для чтения).
- [-] **IDOR в GET /self/api/v1/organization**: Параметры `?id=`, `?org_id=`, `?organization_id=` игнорируются, сервер возвращает данные только из текущей сессии.
- [-] **IDOR / Ролевая модель в `/organizations/{id}/members`**: Эндпоинты существуют, но возвращают `403 Forbidden` при подстановке тестовых ID (`9522951`, `1073626623`). Защита работает.
- [-] **`POST /method/execute` (метод `users.get`)**: Метод существует, но возвращает ошибку `1050` (недостаточно прав / неверный параметр) для профиля `SelfEmployed`. Методы `organizations.getMembersList`, `getInfo`, `get` не существуют (ошибка `3`).
- [-] **IDOR в `/organizations/{id}/members`**: 403 Forbidden.
- [-] **IDOR в `/user` (GET с параметром `?id=` или путем `/user/{id}`)**: Сервер игнорирует параметр или возвращает 403 (данные только из сессии).
- [-] **OAuth Callback (`/oauth/callback`)**: Подмена `code` и `code_verifier` возвращает 400. PKCE защищен.
- [-] **Создание интеграции (`POST /integrations`)**: Возвращает 400 (invalid request / некорректный логотип). Требуется сложная валидация, которую мы не прошли.
- [-] **`/method/execute` (метод `users.get`)**: Ошибка 1050 (недостаточно прав для профиля `SelfEmployed`).
- [-] **Race Condition на создании канала**: Создание канала происходит не через HTTP POST, а через WebSocket (`GET /websocket`, код 101). Для тестирования Race Condition потребуется написание Python-скрипта (asyncio + websockets).

## 🟡 Требует доработки
- [!] **`POST /method/execute`**: Сервер выполняет код, но требует валидный `access_token`. Нужно найти способ получить актуальный токен (из мобильного приложения или через OAuth callback).
- [!] **Origin/Referer Bypass на `/method/auth.validatePhone` (Строка 30)**: Подмена `Origin: https://evil.com` и `Referer: https://evil.com` возвращает `200 OK`. Сервер не проверяет источник запроса. Требуется оценка импакта (возможна CSRF-атака на отправку SMS).