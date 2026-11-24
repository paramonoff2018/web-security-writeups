# Сессия 2026-11-14 (Суббота) - Baseline & First Tests

## 1. Что сделали (Setup)
- [x] Настроен Burp (Scope: ^setka\.ru$ и ^api\.setka\.ru$, Drop out-of-scope).
- [x] Настроен Match and Replace (X_Bug_Bounty, User-Agent Standoff).
- [x] Починен UI Сетки (добавлен wildcard ^.*\.setka\.ru$ в Scope).

## 2. Карта идемпотентности (Idempotency Key)
- Найдено в: POST /reactions.
- Формат: "idempotency_key":"lyxzzzdjs4mwgleek0" (20 символов).
- Результат теста Race Condition (10 запросов залпом):
  - Все 10 запросов вернули 204 No Content.
  - НО счетчик лайков в UI остался 1. 
  - Вывод: Защита работает на уровне БД. Гонки нет.

## 3. TOCTOU (Приватность статуса)
- В UI настройки приватности статуса нет.
- В запросе PUT /users/settings/status/edit передается только status_id и description. Скрытых полей не обнаружено.
- Вывод: Вектор закрыт.

## 4. IDOR (Профили и Чаты)
- При подстановке UUID жертвы в GET /users/{uuid}/education сервер вернул 200 OK, но Content-Type: text/html (SPA-фолбэк). Данных нет.
- При попытке прочитать удаленный чат через API возвращается HTML-каркас.
- Вывод: API отдает данные только через фронтенд, прямые запросы не утекают.

## 5. Mass Assignment
- POST /relations: при передаче role, is_admin сервер вернул 422 Unprocessable Entity.
- PUT /users/settings/personal-data/edit/email: 
  - Можно передать should_send_verification_email: false.
  - Сервер возвращает 200 OK и меняет почту в профиле.
  - НО: вход в аккаунт по номеру телефона, поэтому это не ведет к ATO (Low impact).

## 6. Add-view (Накрутка просмотров)
- Тест POST /posts/{uuid}/add-view: счетчик просмотров не меняется при отправке пачки запросов.

## Итог сессии
Найдено и закрыто 6 векторов. Подтвержденных High/Medium уязвимостей нет. 
Следующая сессия: Логика блокировки (Block/Unblock) и Autorize (GET-only).
