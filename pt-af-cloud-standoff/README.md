# PT AF Cloud — Standoff 365 Bug Bounty

Площадка: The Standoff 365 Bug Bounty
Продукт: PT Cloud Application Firewall (PT Cloud AF) — Positive Technologies
Статус: активная

## Награды
- Всего выплачено: 900 000 ₽
- Средняя: 30 000 ₽
- Принято: 30 / Сдано: 196
- Время до первого ответа: ~20 ч
- Время до решения: ~7,6 дня

## Scope
- `*.ptcloud.ru` и поддомены
- Агент: https://storage.ptsecurity.com/d/9071a220b91d4371809f/
- Тестовое приложение: https://test-ui-megahiddensuffix.ptcloud.ru/

## Цели программы
- Обход защитных механизмов PT Cloud AF
- Нарушение изоляции tenant/customer/folder/domain
- Несанкционированное чтение/изменение политик
- Компрометация консоли управления
- Искажение логов/аналитики/отчётов
- Утечка секретов/ПДн
- Использование AF как точки входа к клиентам/партнёрам/внутренним системам PT
- Недоступность сервисов клиентов

## Структура
- `_program/` — README, SCOPE, RULES, CHECKLIST
- `01..14-*/` — темы (auth, tenant isolation, policy, injection, AF bypass, agents, RCE, secrets, DoS-safe PoC)
- `15-reports/` — финальные отчёты
- `_templates/` — report / poc / checklist
- `_payloads/`, `_notes/` — рабочие материалы
