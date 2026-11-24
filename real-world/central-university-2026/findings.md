# Findings — проверенные векторы

**Формат:** вектор → результат → обоснование.

## 1. Keycloak OAuth — защита

**Проверял:** `response_type` (code/token/id_token), `redirect_uri` (валидный/чужой), implicit flow.

**Результат:**
- implicit flow отключён
- `redirect_uri` whitelist строгий (чужой → 400)
- `token` → 302 error=unauthorized_client

**Вывод:** защита работает. Не баг.

## 2. openid-connect registration — SmartCaptcha

**Проверял:** `POST /realms/central-university/clients-registrations/openid-connect`.

**Результат:** 302 на Yandex SmartCaptcha, `X-Yandex-Captcha: captcha`.

**Вывод:** открытой регистрации нет. Не баг.

## 3. Logout redirect_uri — защита

**Проверял:** `redirect_uri`, `post_logout_redirect_uri` без `id_token_hint`.

**Результат:**
- без `id_token_hint` → 200 HTML (не редирект)
- чужой `post_logout_redirect_uri` → 400

**Вывод:** защита работает. Не баг.

## 4. cu_session после logout — инвалидируется

**Проверял:** `GET /api/hub/avatars/me` со старой кукой после logout.

**Результат:** 401 Unauthorized.

**Вывод:** сессия инвалидируется. Не баг.

## 5. SSO Keycloak после logout my. — закрыт

**Проверял:** Account Console в чистом инкогнито после logout на my.

**Результат:** форма логина.

**Вывод:** SSO-сессия убивается. Не баг.

## 6. IDOR на /competitions/{uuid}/me/state — защита

**Проверял:** чужой UUID из configuration.json и из HAR.

**Результат:** 204 (нет данных) или 404.

**Вывод:** эндпоинт `me/state` не отдаёт чужие данные. Не баг.

## 7. IDOR на /enrollees/{id} — эндпоинт не реализован

**Проверял:** `GET /api/hub/enrollees/{свой UUID}`.

**Результат:** 404.

**Вывод:** есть только `/enrollees/me`. IDOR невозможен. Не баг.

## 8. Admin configurations — UI-конфиг, не баг

**Проверял:** `GET /api/admin/configurations/{key}` (несколько ключей).

**Результат:**
- `GET /api/admin/configurations` без ключа → 403 (защищено)
- `GET /api/admin/configurations/{key}` → 200 UI-конфиг (`type: "UI"`, `value` — нечувствительные данные)

**Вывод:** список защищён, отдельные ключи — публичные для авторизованных. Не баг.

## 9. CSRF на PUT /api/hub/enrollees/me — SameSite=Lax

**Проверял:** `PUT /api/hub/enrollees/me` с `Origin: https://evil.com` и полным JSON.

**Результат:** 200 OK. Сервер не проверяет Origin.

**Но:** `bff.cookie` имеет `SameSite=Lax`, `cu_session` — default Lax в Chrome 2026. **Браузер не отправит куки при cross-site PUT.** CSRF невозможен.

**Вывод:** Origin не проверяется, но SameSite закрывает. Не баг.

## 10. BFF auth-bypass — эндпоинт /bff/ отсутствует

**Проверял:** `/bff/`, `/bff/me`, `/api/bff/`, `/bff/user`, `/bff/config`.

**Результат:** 200 HTML (SPA catch-all) или 404.

**Вывод:** BFF реализован как единый `/api/*`, отдельного `/bff/` нет. Матрица auth-bypass не применима. Не баг.

## 11. Flipt (/flipt/, /api/flipt/) — SPA fallback

**Проверял:** угадывал пути `/flipt/`, `/api/flipt/v1/flags`, `/flipt/health`.

**Результат:** SPA catch-all (одинаковый `Content-Length: 53744`, `Etag: "6abe6949-d1f0"`).

**Вывод:** Flipt не по этим путям. Не баг.

## 12. Hardcoded tokens в JS — публичные по дизайну

**Нашёл в JS-чанках:**
- Bugsnag apiKey (публичный write-only)
- DaData API token (публичный frontend-виджет подсказок адресов)

**Вывод:** оба токена публичные по дизайну. По правилам программы «Разглашение токена Dadata» — **не претендует на вознаграждение**. Не баг.

## Что не проверено (инфраструктура упала)

- `/api/hub/students/me`, `/students/me/experiences/{id}`
- `/api/micro-lms/courses/{id}/students/{id}`
- `/api/appointment-service/interviewers/user-info?email=`
- `/api/appointment-service/interviewers/{id}` PUT
- `/api/certificates/user-certificates/me/published`
- `/api/notification-hub/notifications/in-app/read` POST

12 октября 2026 Yandex Cloud (в котором хостится CU) был атакован — **`/api/hub/*` и `/api/admin/*` легли в 502**. До восстановления — невозможно проверить.
