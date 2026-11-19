# Web Security Writeups

Разборы PortSwigger Web Security Academy + real-world engagements.

**Автор:** [@paramonoff2018](https://github.com/paramonoff2018)

## Прогресс

### PortSwigger Web Security Academy

| Тема | Пройдено | Всего |
|---|---|---|
| [CSRF](./csrf/) | 1 | 8 |
| [SQL Injection](./sqli/) | 2 | 18 |
| [XSS](./xss/) | 1 | 30 |
| [Access Control](./access-control/) | 0 | 13 |
| [Authentication](./authentication/) | 1 | 14 |
| [API testing](./api-testing/) | 2 | 5 |
| [Web LLM Attacks](./web-llm-attacks/) | 2 | 3 |
| [Web Cache Deception](./web-cache-deception/) | 2 | 13 |
| [Path Traversal](./path-traversal/) | 1 | 6 |
| [NoSQL Injection](./nosql-injection/) | 1 | 4 |
| [Race Conditions](./race-conditions/) | 2 | 6 |
| [XML External Entity (XXE)](./xxe/) | 1 | 9 |

**Всего:** 16 / 129

_Последнее решённое: XSS → Reflected XSS в HTML-контексте без кодирования — `<script>alert(1)</script>` через `?search=`, сервер вставляет в HTML as-is._

### Real-World Bug Bounty

| Программа | Период | Векторов проверено | Найдено |
|---|---|---|---|
| [Central University (Т-Банк)](./real-world/central-university-2026/) | окт 2026 | 12 | 0 |

## Структура

- csrf/ — Cross-Site Request Forgery
- sqli/ — SQL Injection
- xss/ — Cross-Site Scripting
- access-control/ — контроль доступа
- authentication/ — аутентификация
- api-testing/ — API testing (документация, скрытые эндпоинты)
- web-llm-attacks/ — атаки на интеграции LLM (prompt injection, excessive agency)
- web-cache-deception/ — обман веб-кэша (path mapping, static extension, delimiters)
- path-traversal/ — обход файловых путей
- nosql-injection/ — NoSQL Injection (MongoDB)
- race-conditions/ — Race Conditions (гонки состояний)
- xxe/ — XML External Entity Injection
- real-world/ — разборы реальных bug bounty программ
- templates/ — шаблон write-up'а

## Disclaimer

Все материалы — публичная информация. Никаких куки, токенов, PII, внутренних ID. Engagement проводился в рамках правил публичной bug bounty программы.
