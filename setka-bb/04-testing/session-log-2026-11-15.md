# Сессия 2026-11-15 (Воскресенье) - Authz & Logic Tests

## 1. Education / Career (IDOR)
- Проверено через Repeater и Autorize (User B).
- Ответ для чужого профиля возвращает HTML-каркас с заглушкой ("пока ничего нет").
- Вывод: Защита работает, данные не утекают.

## 2. Block/Unblock (Broken Access Control)
- Эндпоинты: POST /users/{uuid}/block и POST /users/{uuid}/unblock.
- Попытка IDOR (Б разблокирует А): сервер вернул 204 No Content, но блокировка в БД не снялась (проверено в UI).
- Попытка Б разблокировать себя: 400 Bad Request ("нельзя подписаться/отписаться на/от самого себя").
- Вывод: Логика защищена, IDOR нет.

## 3. Race Condition (Реакции / Idempotency)
- Проверено: отправка POST /reactions с разными idempotency_key (5 запросов).
- Все запросы вернули 204 No Content.
- Счетчик лайков остался 1 (дубликаты отсекаются на уровне БД по связке user_id + entity_id).
- Вывод: Защита от накрутки работает.

## Итог сессии
Проверено 5 векторов (IDOR, Access Control, Race, Mass Assignment, Logic).
Подтвержденных High/Medium уязвимостей нет. Базовая защита API работает корректно.
