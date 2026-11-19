# Avito — Bug Bounty (Bi.Zone)

Площадка: Bi.Zone Bug Bounty
Продукт: Avito (web, mobile, API, HR-сервисы)
Статус: активная

## Критичные активы (critical, выплачивается)
- android / ios apps — [ссылки](https://www.avito.ru/journal/tools/app)
- api.avito.ru
- m.avito.ru
- payments.avito.ru
- www.avito.ru

## Высокие активы (high, выплачивается)
- *.hrbt.ru — HRM
- *.hmsg.me — HRM
- hrmka.ru — HRM
- *.haraba.ru — Haraba
- *.maxposter.ru — Maxposter
- *.hrmessenger.com — HRM
- *.autoteka.ru
- *.avito.ru — все остальные ресурсы на *.avito.ru

## Что искать (in-scope)
RCE, SQLi, XXE, SSRF, Broken Auth, XSS, IDOR, Privilege Escalation,
ошибки авторизации, open redirect, обход лимитов бесплатных операций,
утечки ПДн (телефоны, VIN, платёжка).

## Что НЕ рассматривается
См. `_program/SCOPE.md` (Out-of-scope) и `_program/RULES.md`.

## Структура
- `_program/` — README, SCOPE, RULES, CHECKLIST
- `01..11-*/` — темы по категориям уязвимостей
- `12-reports/` — финальные отчёты
- `_templates/` — шаблоны отчёта, PoC, чек-листа
- `_payloads/`, `_notes/` — рабочие материалы
