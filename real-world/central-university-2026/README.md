# Central University Bug Bounty — engagement

**Hunter:** @paramonoff2018 (Al_x_Pv)
**Программа:** Central University (Т-Банк), публичная на платформе Т-Банка
**Период:** 4–12 октября 2026
**Scope:** my.centraluniversity.ru, id.centraluniversity.ru, cu.ru
**Правила:** 5 req/s, X-Bug-Bounty header, только свои аккаунты

## Кратко

- 8 дней, ~25 часов активной работы
- Стек: Angular 21 + SSR, ASP.NET Core BFF, Keycloak, Yandex SmartCaptcha, Yandex Cloud LB
- Записан HAR (1942 запроса, 93 МБ), проанализировано 620 JS-чанков
- Проверено 12+ векторов: OAuth, SSO, CSRF, IDOR, mass assignment, BFF auth-bypass, SSRF, session management
- **Найдено уязвимостей: 0**
- **Закрыто векторов: 12** (с обоснованием почему не уязвимо)

## Зачем публиковать «0 багов»

Реальный bug bounty — это 90% «не баг». Ценность write-up — **показать методологию**: как строить разведку, где искать, как проверять гипотезы, как **остановиться и не писать отчёт без impact**.

## Навигация

- [`methodology.md`](./methodology.md) — подход, tooling, workflow
- [`findings.md`](./findings.md) — все проверенные векторы и результаты
- [`lessons.md`](./lessons.md) — что забираю в следующие программы
