# XSS — Avito

## Что ищем
Cross-Site Scripting — stored, reflected, DOM-based.

## Где искать (Stored)
- Объявления: заголовок, описание, характеристики
- Отзывы и рейтинги
- Чат: сообщения, вложения, превью ссылок
- Профиль: имя, город, "о себе"
- HR-системы: резюме, вакансии, комментарии
- autoteka.ru: комментарии к отчётам

## Где искать (Reflected)
- Поиск (`q=` в URL)
- Ошибки (404, 500 с параметром в тексте)
- Редиректы с параметром
- API-ответы с отражением

## Где искать (DOM-based)
- `location.hash`, `location.search`, `document.referrer`
- `innerHTML`, `eval`, `document.write`
- SPA-роутинг (React Router, Vue Router)
- postMessage без проверки origin

## Payload'ы
```html
<script>alert(document.domain)</script>
<img src=x onerror=alert(document.domain)>
<svg onload=alert(document.domain)>
javascript:alert(document.domain)
"><script>alert(1)</script>
```

## Обходы WAF
- `<img src=x onerror=alert(1)>` (без script)
- `<svg/onload=alert(1)>`
- `<details open ontoggle=alert(1)>`
- Unicode/HTML-entities: `&#x3c;script&#x3e;`
- Смешанный регистр: `<ScRiPt>`
- Без скобок: `<script>alert\`1\`</script>`

## Out-of-scope
- **Self-XSS** без возможности атаки на другого пользователя
- **Отсутствие security headers** (CSP, X-XSS-Protection) — не считается
- **Clickjacking**
- XSS только в устаревших браузерах

## Инструменты
- Burp + XSStrike
- Dalfox
- DOM Invader (Burp)

## Чек-лист
- [ ] Найти все точки отражения ввода
- [ ] Проверить stored в объявлениях, отзывах, чатах
- [ ] Проверить reflected в поиске, ошибках
- [ ] Проверить DOM-based в SPA (source → sink)
- [ ] Проверить обходы WAF, если есть фильтрация
- [ ] Проверить, что payload исполняется в контексте другого пользователя (не self-XSS)

## Не делать
- Не использовать реальные аккаунты пользователей
- Не спамить XSS-ссылками
- В PoC — `alert(document.domain)`, не `alert(1)` (чтобы показать домен)
