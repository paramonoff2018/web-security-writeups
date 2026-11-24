# Recon — PT AF Cloud

## Scope (Standoff 365)
- `*.ptcloud.ru` и поддомены
- Агент: https://storage.ptsecurity.com/d/9071a220b91d4371809f/
- Тестовое приложение: https://test-ui-megahiddensuffix.ptcloud.ru/
- Вне scope, но можно отправить: уязвимости, прямо влияющие на PT Cloud AF / клиентов

## Архитектура (что нужно понять)
- **Control plane** — консоль управления, API, политики, tenant-модель
- **Border** — компонент, применяющий политики к трафику
- **Agent** — фильтрация трафика на стороне клиента
- **Tenant / customer / folder / domain** — уровни изоляции
- **Тестовый tenant** — выделенная среда для безопасных PoC

## Что собираем
- Поддомены *.ptcloud.ru (subfinder + httpx)
- Эндпоинты консоли управления (JS-бандлы, GraphQL introspection)
- API control plane (`/api/v1/...`, `/v1/...`)
- Роли и permissions (admin, analyst, viewer)
- Скачать агент, распаковать, изучить (Go/Rust? бинарь? конфиги?)
- Тестовое приложение: какие эндпоинты, какие правила AF на нём висят

## Инструменты
- subfinder, httpx, katana, gau
- Burp + InQL (GraphQL)
- Ghidra / IDA (агент)
- jq (для API-ответов)

## Чек-лист
- [ ] subfinder по *.ptcloud.ru
- [ ] httpx -title -tech-detect
- [ ] Скачать агент, распаковать, вытащить строки/конфиги/эндпоинты
- [ ] Разобрать консоль управления (JS, GraphQL)
- [ ] Разобрать тестовое приложение test-ui-megahiddensuffix
- [ ] Составить схему: control plane ↔ border ↔ agent ↔ tenant

## Осторожно
- Не сканировать инфраструктуру клиентов AF
- Не трогать реальные приложения
- Никаких массовых рестартов agents/borders
