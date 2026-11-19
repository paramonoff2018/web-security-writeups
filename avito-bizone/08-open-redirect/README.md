# Open Redirect — Avito

## Что ищем
Open redirect **без промежуточной страницы переадресации** (явно указано в правилах Avito).

## Где искать
- Параметры `redirect`, `redirect_uri`, `return`, `returnUrl`, `next`, `url`, `goto`, `target`, `continue`
- OAuth: `redirect_uri`, `callback`
- Logout: `?next=`
- Восстановление пароля: `?return=`
- Мобильные приложения: deeplink'и, custom scheme
- HR-системы: редирект после логина

## Базовые payload'ы
```
https://www.avito.ru/redirect?url=https://evil.com
https://www.avito.ru/redirect?url=//evil.com
https://www.avito.ru/redirect?url=https:evil.com
https://www.avito.ru/redirect?url=\\evil.com
https://www.avito.ru/redirect?url=https://www.avito.ru.evil.com
https://www.avito.ru/redirect?url=javascript:alert(1)
```

## Обходы allow-list
- `https://evil.com#@avito.ru`
- `https://avito.ru@evil.com`
- `https://evil.com?avito.ru`
- `//evil.com` (protocol-relative)
- Unicode/percent-encoding: `%2f%2fevil.com`, `%5cevil.com`
- Тройной слэш: `///evil.com`

## Out-of-scope
- **Редирект с промежуточной страницей** «Вы покидаете Avito» — не считается
- Редирект на тот же домен
- Открытый редирект без возможности атаки (например, только на 404)

## Инструменты
- Burp + OpenRedirect scanner
- Ручной перебор через ffuf

## Чек-лист
- [ ] Найти все параметры редиректа (grep по JS-бандлам)
- [ ] Подставить `https://evil.com` → проверить 302
- [ ] Попробовать обходы allow-list
- [ ] Проверить OAuth `redirect_uri`
- [ ] Проверить мобильные deeplink'и
- [ ] Убедиться, что нет промежуточной страницы

## Не делать
- Не использовать редирект для фишинга
- В PoC — только `302 Location: https://evil.com`
