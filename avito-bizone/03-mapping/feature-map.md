# Feature Map — Карта эндпоинтов

## Методология
1. Пройтись по основному функционалу приложения (web, mobile web)
2. Записать каждый эндпоинт: метод, URL, параметры, тело запроса
3. Отметить потенциально опасные места (ID, суммы, роли, статусы)
4. Проверить GraphQL (если есть) через /graphql, /v1/graphql

## Таблица

| # | Фича | Метод | URL | Параметры (GET/POST) | Примечание | Статус |
|---|------|--------|-----|----------------------|------------|--------|
| 1 | Поиск объявлений | GET | /api/1.0/items | q, category, location, user_id? | IDOR: user_id | ⏳ |
| 2 | Просмотр объявления | GET | /api/1.0/items/{id} | item_id | IDOR | ⏳ |
| 3 | Создание объявления | POST | /api/1.0/items | JSON: title, price, category_id | Race | ⏳ |
| 4 | Редактирование объявления | PUT/PATCH | /api/1.0/items/{id} | JSON: ... | Authz | ⏳ |
| 5 | Удаление объявления | DELETE | /api/1.0/items/{id} | item_id | IDOR+Authz | ⏳ |
| 6 | Оплата/пополнение | POST | /payments.avito.ru/... | amount, user_id | Race (двойное списание) | ⏳ |
| 7 | Промокод/купон | POST | /api/1.0/coupons | code | Race (двойное применение) | ⏳ |
| 8 | Лайк/избранное | POST | /api/1.0/favorites | item_id | Race (дублирование) | ⏳ |
| 9 | Регистрация | POST | /api/1.0/auth/register | phone, email | Rate limit bypass | ⏳ |
| 10 | Восстановление пароля | POST | /api/1.0/auth/reset | phone/email | OTP brute | ⏳ |
| 11 | Чат/сообщения | WS/GET/POST | /api/1.0/messages | chat_id, user_id | IDOR чужих чатов | ⏳ |
| 12 | AI-ассистент «Ави» | POST | /api/1.0/ai/chat | prompt, session_id | LLM injection | ⏳ |
| 13 | AI-ассистент «Ави Pro» | POST | /api/1.0/ai/pro/chat | prompt | LLM injection priv | ⏳ |
| 14 | HR-чат-бот | POST | *.hrmessenger.com/... | message | LLM injection | ⏳ |

> ⏳ — не проверено | ✅ — проверено | ❌ — не уязвимо | 🚨 — найдена уязвимость