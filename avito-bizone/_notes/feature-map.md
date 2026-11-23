# Feature Map — Карта эндпоинтов (Avito)

> Живая карта: фичи → эндпоинты → параметры. Обновляй по мере разведки.

## Методология
1. Пройтись по функционалу (web + mobile web) через Burp
2. Записать: метод, URL, параметры, тело запроса
3. Отметить опасные места (ID, суммы, роли, статусы)
4. Проверить GraphQL (`/graphql`, `/v1/graphql`)

## Таблица

| # | Фича | Метод | URL | Параметры | Гипотеза | Статус |
|---|------|--------|-----|-----------|----------|--------|
| 1 | Поиск объявлений | GET | /api/1.0/items | q, category, location | IDOR: user_id | ⏳ |
| 2 | Просмотр объявления | GET | /api/1.0/items/{id} | item_id | IDOR | ⏳ |
| 3 | Создание объявления | POST | /api/1.0/items | title, price, category_id | Race | ⏳ |
| 4 | Редактирование объявления | PUT/PATCH | /api/1.0/items/{id} | JSON | Authz | ⏳ |
| 5 | Удаление объявления | DELETE | /api/1.0/items/{id} | item_id | IDOR+Authz | ⏳ |
| 6 | Оплата/пополнение | POST | payments.avito.ru/... | amount, user_id | Race | ⏳ |
| 7 | Промокод/купон | POST | /api/1.0/coupons | code | Race (limit overrun) | ⏳ |
| 8 | Лайк/избранное | POST | /api/1.0/favorites | item_id | Race | ⏳ |
| 9 | Регистрация | POST | /api/1.0/auth/register | phone, email | limit bypass | ⏳ |
| 10 | Сброс пароля | POST | /api/1.0/auth/reset | phone/email | OTP | ⏳ |
| 11 | Чат/сообщения | WS/POST | /api/1.0/messages | chat_id, user_id | IDOR | ⏳ |
| 12 | AI «Ави» | POST | ai-ассистент | prompt, session_id | LLM injection | ⏳ |
| 13 | AI «Ави Pro» | POST | ai-pro | prompt | LLM priv | ⏳ |
| 14 | HR-бот (hrmessenger) | POST | *.hrmessenger.com | message | LLM injection | ⏳ |

## Легенда статусов
- ⏳ не проверено
- ✅ проверено, не уязвимо
- 🚨 найдена уязвимость (детали в 12-reports/)