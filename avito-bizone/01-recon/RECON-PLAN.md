# Recon Plan — Avito (Bi.Zone)

**Обновлено:** 2026-11-21
**Статус:** IN PROGRESS
**Стек:** Burp Community, Kali

## Фаза 0. Scope & Rules
- In-scope: см. `../_program/SCOPE.md`
- Out-of-scope: см. `../_program/OUT-OF-SCOPE.md`
- Два тестовых аккаунта: см. `../_notes/ACCOUNTS.md`

## Фаза 1. Пассивная разведка (без трафика в цель)
### 1.1 Поддомены
- subfinder, assetfinder, amass, findomain
- crt.sh (Certificate Transparency)
- Готовый снимок (2026-08-10): 157 поддоменов, включая `adm.avito.ru`, `bi-test.avito.ru`, `business.avito.ru`, `api-ast-to-hd.avito.ru`

### 1.2 JS-файлы и historical URLs
- waybackurls, gau, katana
- LinkFinder, jsluice, SecretFinder

### 1.3 GitHub / GitLab
- github-subdomains, ручной поиск по коду
- Не репортить «секрет без влияния»

## Фаза 2. Активная разведка (точечно)
### 2.1 Резолвинг и живость
- puredns, httpx

### 2.2 Технологии
- whatweb, Wappalyzer

### 2.3 Порты
- naabu, top-1000, только на подтверждённых хостах

### 2.4 Скриншоты
- Aquatone / EyeWitness

## Фаза 3. API-разведка
- api.avito.ru: OAuth2, OpenAPI-снапшот 248 путей / 256 операций
- Поиск скрытых эндпоинтов из JS и wayback
- Проверка авторизации: cross-account (2 аккаунта)

## Фаза 4. Мобильное приложение (только при обосновании)
- com.avito.android
- Только если веб не даёт ответа по конкретному вектору
- mitmproxy, apktool, Frida (root/jailbreak)

## Фаза 5. Поиск уязвимостей
- Категории: см. папки `02-auth-session` … `11-privilege-escalation`
- Burp Community: Proxy, Repeater, Intruder (throttle, точечно)
- nuclei с осторожными шаблонами
- ffuf с маленькими словарями

## Фаза 6. Отчётность
- Шаблоны: `../_templates/`
- Обезличивание: без чужих ПДн, номеров, токенов

## Приоритетные цели (первая неделя)
1. `adm.avito.ru` — админка
2. `bi-test.avito.ru` — тестовый стенд
3. `api.avito.ru` — IDOR-кандидаты (user_id/item_id/chat_id)
4. `business.avito.ru` — лимиты
5. AI-сервисы (HR Messenger, HRMOST, Автохаб, Haraba)

## Ежедневный ритуал
- Утро: пассив (crt.sh, wayback, GitHub) — 30 мин
- День: ручное тестирование в Burp по 1–2 приоритетным хостам
- Вечер: обновить `_notes/` и `_program/CHECKLIST.md`

## Фаза 5.4. Race Conditions (гонки)
- Памятка: `RACE-CONDITIONS.md`
- Ключевые цели: OAuth token store, лимиты публикаций, купоны/промо, платежи (только тест), рейтинги/лайки
- Инструменты: Burp Repeater "Send group in parallel", Turbo Intruder (single-packet attack), racey, curl --parallel
- Приоритет: **высокий**, потому что сканеры это не видят, а импакт может быть финансовым
