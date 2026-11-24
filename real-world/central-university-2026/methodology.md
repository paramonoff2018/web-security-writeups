# Methodology

## Tooling

- **Burp Suite Community** — перехват, Repeater, Match&Replace (X-Bug-Bounty), scope
- **Chrome DevTools** — Network, Application (cookies), Sources (JS)
- **FoxyProxy** — проксирование только целевых доменов
- **curl + jq** — работа с HAR, извлечение API-карты
- **grep / LinkFinder** — поиск эндпоинтов в JS
- **Python + venv** — скрипты для массовых проверок (с rate limit)

## Workflow

### 1. Recon (день 1)
- `subfinder -d centraluniversity.ru` → 57 поддоменов
- `httpx` → 13 живых
- Scope: 3 цели (my., id., cu.ru)

### 2. Stack fingerprinting (день 1)
- `whatweb` + DevTools
- Angular 21 + SSR, ASP.NET Core BFF, Keycloak, Yandex SmartCaptcha

### 3. HAR → API-карта (дни 3–4)
- Записал HAR (1942 запроса, 93 МБ) через DevTools → Network → Preserve log
- `jq` → извлёк 55 уникальных API-эндпоинтов
- Группировка: auth, hub, admin, lms, notification-hub, appointment, certificates

### 4. JS-анализ (дни 4–8)
- Скачал 620 JS-чанков через `curl` с rate limit
- `grep` по паттернам: пути `/api/...`, имена полей (`role`, `status`, `userId`)
- Найдены **новые модули**, которых не было в HAR: `appointment-service`, `referrals`, `micro-lms`

### 5. Testing (дни 4–8)
- Каждая гипотеза: **2 часа максимум**, потом — закрываем
- Repeater: эталон + вариации (без куки, чужой ID, X-Forwarded-For)
- Каждый запрос — `Copy as cURL` из Chrome, чтобы не ошибиться с куками

## Принципы

1. **Не писать отчёт без impact в одном предложении.** «Отсутствие флагов куки» — не баг.
2. **Один вектор — 2 часа.** Не распыляться.
3. **Не отправлять PUT/POST с чужим body.** Может стереть свои данные.
4. **5 req/s всегда.** Даже если сервер быстрый.
5. **Не трогать чужие аккаунты.** Только свои + явные PoC.

## Инструменты, которые НЕ применял

- `nuclei` — автоскан запрещён правилами
- `ffuf` — только точечно, не по словарям
- `nmap` — открытые порты не в скоупе
- `sqlmap` — не нашли SQLi-поверхностей
