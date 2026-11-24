# Handoff — Avito Bug Bounty (Bi.Zone)

> Точка входа для агента в начале каждой сессии.
> Читай этот файл ПЕРВЫМ, затем scope.txt, out_of_scope.txt,
> последний отчёт в reports/ и audit_rules.md.

## Текущий статус
- Программа: Avito (Bi.Zone Bug Bounty)
- Хантер: Al_x_Pv (заголовок `X-Bug-Bounty: Al_x_Pv`)
- Стадия: RECON (пассивная разведка) — первый прогон

## Скоуп (кратко)
- critical: www.avito.ru, api.avito.ru, m.avito.ru, payments.avito.ru, mobile apps
- high: *.hrbt.ru, *.hmsg.me, hrmka.ru, *.haraba.ru, *.maxposter.ru, *.hrmessenger.com, *.autoteka.ru, *.avito.ru
- AI/LLM (приоритет): ассистенты «Ави»/«Ави Pro», HR Messenger, HRMOST, Автохаб, Haraba

## Приоритетные векторы (по интересам хантера)
1. Race Conditions (купоны, лимиты, OAuth token store) — см. 01-recon/RACE-CONDITIONS.md
2. IDOR / BOLA (user_id, item_id, chat_id)
3. LLM injection (ассистенты «Ави»/«Ави Pro»)
4. Privilege Escalation (mass assignment, JWT claims)

## Что уже сделано
- [x] Каркас проекта (scope, rules, env, gitignore, filter_noise.py)
- [ ] Пассивный enum поддоменов (subfinder) — ПЕРВЫЙ ШАГ
- [ ] Резолвинг + tech-detect (httpx)
- [ ] Well-known эндпоинты

## Следующий шаг (для агента)
1. subfinder -d avito.ru (и остальные корневые домены) с rate limit
2. httpx -l subs.txt -title -tech-detect -status-code
3. Сохранить сырьё в raw_logs/, выжимку в filtered/
4. Обновить отчёт за сегодня в reports/

## Ограничения (напоминание)
- Только домены из scope.txt
- Rate limit ≤ 2 RPS
- Весь трафик через Burp proxy 127.0.0.1:8080
- Не DELETE / массовые POST без подтверждения
- Креды/токены только из .env, не в отчёты
