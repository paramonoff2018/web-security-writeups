# SQL Injection — Avito

## Что ищем
SQLi в поиске, фильтрах, сортировке, API-параметрах, GraphQL-аргументах.

## Где искать
- Поиск по объявлениям (`q=`, `query=`, `search=`)
- Фильтры: категории, цена, регион, параметры авто (`brand=`, `model=`, `year=`)
- Сортировка (`sort=price_asc`, `order_by=`)
- Пагинация (`limit=`, `offset=`, `page=`)
- GraphQL: аргументы резолверов, `orderBy`, `where`
- HR-системы (*.hrbt.ru, hrmka.ru) — поиск по сотрудникам, вакансиям
- autoteka.ru — поиск по VIN

## Типы инъекций
- **Классическая:** `' OR 1=1--`
- **Blind boolean:** `' AND 1=1--` vs `' AND 1=2--`
- **Blind time-based:** `'; WAITFOR DELAY '0:0:5'--` (MSSQL), `pg_sleep(5)` (Postgres), `SLEEP(5)` (MySQL)
- **Union-based:** `' UNION SELECT NULL,NULL--`
- **Stacked queries:** `'; DROP TABLE--` (только PoC, никогда на реальных данных!)
- **Out-of-band:** DNS/HTTP через `xp_dirtree`, `LOAD_FILE`, `COPY TO PROGRAM`

## Ограничения Avito
- **Никаких массовых выгрузок** через SQLi — только PoC на 1 строку (например, `SELECT @@version`)
- **Никаких destructive queries** (DROP, DELETE, UPDATE)
- В отчёте — только подтверждение инъекции, без дампа таблиц

## Инструменты
- sqlmap (с `--risk=1 --level=1`, без `--dump`)
- Burp + Intruder с кастомными payload'ами
- Ручные тесты через curl/Postman

## Чек-лист
- [ ] Найти параметры, влияющие на SQL-запросы (поиск, фильтры, сортировка)
- [ ] Проверить `'`, `"`, `\`, `)`, `;` — есть ли ошибки/изменения
- [ ] Blind boolean: сравнить ответы при `AND 1=1` vs `AND 1=2`
- [ ] Time-based: замерить задержку при `pg_sleep(5)` (максимум 5 сек!)
- [ ] Проверить GraphQL-аргументы
- [ ] Проверить заголовки (X-Forwarded-For, User-Agent, Referer)

## Не делать
- Не использовать `--dump`, `--all`, `--os-shell`
- Не запускать sqlmap в `--risk=3 --level=5` (это фактически DoS)
- Не выгружать пользовательские данные
