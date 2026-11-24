# XSS — PT AF Cloud

## Что ищем
Stored XSS или другое сохранённое внедрение активного контента в консоли управления, позволяющее:
- выполнять действия от имени пользователя
- менять настройки защиты
- закрепляться в интерфейсе управления

## Где искать (Stored)
- Название tenant / customer / folder / domain
- Название policy / rule / rule-set
- Описание инцидента / отчёта / рекомендации
- Комментарии к инцидентам
- Имена пользователей / роли
- Импортированные правила (поле description)
- Названия сертификатов
- Логи / события (если рендерятся без экранирования)
- Уведомления (email / webhook preview)

## Где искать (Reflected / DOM)
- Поиск по правилам / инцидентам
- Ошибки с отражением параметра
- SPA-роутинг (React / Vue / Angular)
- `postMessage` без проверки origin
- `innerHTML` в отчётах / превью

## Payload'ы
```html
<script>alert(document.domain)</script>
<img src=x onerror=alert(document.domain)>
<svg onload=alert(document.domain)>
<details open ontoggle=alert(document.domain)>
```

## Цепочки (важно для PT)
- **XSS → CSRF-токен** → действие от имени админа (смена политики)
- **XSS → кража сессии** → полный захват консоли (если нет HttpOnly — но это отдельно out-of-scope по заголовкам; тут важна сама возможность XSS)
- **XSS → закрепление в интерфейсе** (persistence через правило с payload в description)

## Out-of-scope
- Self-XSS без атаки на другого пользователя
- Отсутствие CSP / X-XSS-Protection (не считается)
- Clickjacking
- XSS только в устаревших браузерах

## Инструменты
- Burp + XSStrike
- Dalfox
- DOM Invader

## Чек-лист
- [ ] Найти все точки отражения пользовательского ввода
- [ ] Проверить stored в названиях tenant / policy / rule / инцидента
- [ ] Проверить DOM-based в SPA
- [ ] Проверить postMessage
- [ ] Проверить обход WAF (если есть)
- [ ] Показать цепочку: XSS → действие от имени пользователя (смена политики)

## Не делать
- Не атаковать реальных пользователей
- Не спамить payload'ами
- В PoC — `alert(document.domain)`, не `alert(1)`
