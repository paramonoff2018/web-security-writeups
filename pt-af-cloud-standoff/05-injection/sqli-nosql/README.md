# SQL / NoSQL Injection — PT AF Cloud

## Что ищем
SQL/NoSQL-инъекции в интерфейсах настройки, поиска, фильтрации, экспорта и управления правилами.

## Где искать
- Поиск по правилам / политикам / инцидентам / отчётам
- Фильтры (по tenant, domain, severity, дате)
- Сортировка (`sort=`, `order=`)
- Экспорт (CSV, PDF, JSON) — параметры фильтра
- Пагинация (`limit=`, `offset=`)
- GraphQL: аргументы `where`, `orderBy`, `filter`
- API конфигурации: параметры применения политик

## Типы
- **SQL:** `' OR 1=1--`, blind boolean/time, union-based, stacked
- **NoSQL (MongoDB):** `{"$ne": null}`, `{"$gt": ""}`, `{"$regex": "^a"}`
- **NoSQL (Redis / Elasticsearch):** wildcard / script injection
- **GraphQL:** инъекция в аргументы резолверов

## Ограничения PT
- **Никаких destructive queries** (DROP, DELETE, UPDATE)
- **Никакой массовой выгрузки** (только PoC: `SELECT version()` / 1 документ)
- **Никаких DoS-векторов** (heavy queries, time-based > 5 сек)
- PoC — только чтение

## Инструменты
- sqlmap (`--risk=1 --level=1`, без `--dump`)
- NoSQLMap
- Burp + Intruder
- GraphQL Voyager

## Чек-лист
- [ ] Найти параметры, влияющие на запросы (поиск, фильтры, сортировка, экспорт)
- [ ] Проверить `'`, `"`, `\`, `)`, `;` — ошибки/изменения
- [ ] Blind boolean: `AND 1=1` vs `AND 1=2`
- [ ] Blind time: `pg_sleep(5)` (максимум 5 сек!)
- [ ] NoSQL: `{"$ne": null}` в JSON-теле
- [ ] GraphQL: инъекция в `where`/`orderBy`
- [ ] Проверить заголовки (X-Forwarded-For, User-Agent)

## Не делать
- Не `--dump`, `--all`, `--os-shell`
- Не `--risk=3 --level=5`
- Не выгружать чужие правила / политики / отчёты
