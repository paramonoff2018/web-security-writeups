# Recon Plan — PT AF Cloud (Standoff 365)

**Обновлено:** 2026-11-21
**Статус:** IN PROGRESS
**Стек:** Burp Community, Kali, WinServer-lab (VB)

## 🎯 Ключевая особенность
Это не поиск уязвимостей в коде приложения. Это **тестирование самого WAF**: обход фильтрации, ошибки в control plane, нарушение изоляции тенантов, уязвимости агентов.

## Фаза 0. Scope & Rules
- In-scope: `*.ptcloud.ru`, тестовые приложения (`test-ui-megahiddensuffix.ptcloud.ru`), агенты
- Out-of-scope: см. `../_program/OUT-OF-SCOPE.md`
- **Запрещено:** DoS/DDoS, resource exhaustion, массовые рестарты, атаки на реальных клиентов, pivot во внутреннюю инфраструктуру
- Демо-портал для изучения интерфейса: `demo.ptcloud.ru`

## Фаза 1. Пассивная разведка
### 1.1 Поддомены
- crt.sh, subfinder, assetfinder, amass
- Снимок (2026-05-09): 52 поддомена, включая `af.ptcloud.ru`, `auth.ptcloud.ru`, `grafana.infra.ptcloud.ru`, `test-ui-megahiddensuffix.ptcloud.ru`

### 1.2 JS-файлы и endpoints
- waybackurls, gau, katana
- LinkFinder, jsluice, SecretFinder

### 1.3 GitHub / публичные источники
- Поиск `ptcloud.ru` в публичном коде
- Writeups: Codeby, Habr, Standoff 365

## Фаза 2. Активная разведка
- httpx, whatweb, Wappalyzer
- Aquatone / EyeWitness — скриншоты
- naabu (точечно, top-1000)

## Фаза 3. WAF Bypass (основной фокус)
- Памятка: `BYPASS-MEMO.md`
- Парсерные дифференциалы: PHP vs ASP.NET, HPP, нормализация
- HTTP/2: stream confusion, downgrade, H2.CL/H2.TE
- Chunked transfer, сжатие, WebSocket, gRPC
- Кодировки: double URL-encoding, Unicode, null bytes, overlong UTF-8
- Path normalization, mixed case, uncommon separators
- **Демо-портал** `demo.ptcloud.ru` — безопасная среда для проверки гипотез

## Фаза 4. API и консоль управления
- Auth: обход входа, эскалация, session/token
- Stored XSS в интерфейсе управления
- Injection: SQL/NoSQL/LDAP/template/command в настройках, поиске, экспорте
- SSRF в функциях консоли, API, control plane
- Утечка секретов через телеметрию, debug endpoints

## Фаза 5. Изоляция тенантов
- Доступ к объектам другого tenant/customer/folder/domain
- Чтение чужих отчётов, инцидентов, рекомендаций
- Несанкционированное изменение/отключение политики чужого тенанта

## Фаза 6. Агенты и border
- RCE, выход из sandbox, чтение локальных секретов
- Утечка данных клиента: трафик, заголовки, cookies, токены, конфиги
- **Плавное применение конфигурации по группам** — потенциальная цель для race condition / DoS-safe PoC

## Фаза 7. Отчётность
- Шаблоны: `../_templates/`
- Обязательно: PoC, сценарий атаки, рекомендации
