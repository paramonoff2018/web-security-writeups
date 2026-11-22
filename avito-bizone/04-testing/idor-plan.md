# IDOR / BOLA — План тестирования

## Гипотезы

### Прямой IDOR (числовой ID)
Попробовать подставить чужой `item_id`, `user_id`, `order_id`, `chat_id`:
- GET `/api/1.0/items/{id}` — чужие объявления
- GET `/api/1.0/users/{id}/profile` — чужие профили
- GET `/api/1.0/orders/{id}` — чужие заказы
- GET `/api/1.0/messages/{chat_id}` — чужие чаты
- GET `/api/1.0/favorites/{user_id}` — чужие избранные
- GET `/payments.avito.ru/.../transactions/{txn_id}` — чужие транзакции

### UUID / хэш (если не угадать, может быть утечка в другом месте)
- Может быть IDOR через referral link (ссылка «поделиться»)
- Может быть IDOR через WebSocket (чат в реальном времени)
- Может быть IDOR через массовую выгрузку (export CSV/PDF)

### Blind IDOR
- Изменить параметр в теле запроса, ответить может 200 OK с другими данными
- Ответ может содержать чужие данные в поле `next` / `prev` / `related`

## Инструменты
- Burp Intruder (Pitchfork / Sniper) для перебора ID
- Burp Repeater для ручной проверки
- Autorize extension (автоматическая проверка: запрос от User A → User B)

## Сценарий
1. Войти как User 1, перехватить запрос с ID
2. Войти как User 2, повторить тот же запрос с тем же ID
3. Если User 2 получает данные User 1 → IDOR
4. Проверить различные методы: GET → IDOR read, PUT/PATCH/DELETE → IDOR write

> Результаты тестов заносить: `05-findings/idor-*.md`