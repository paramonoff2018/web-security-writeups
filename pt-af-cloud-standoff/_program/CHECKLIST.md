# PT AF Cloud — сводный чек-лист

## Recon
- [ ] Поддомены *.ptcloud.ru
- [ ] Скачать и разобрать агент (storage.ptsecurity.com/d/9071a220b91d4371809f/)
- [ ] Разведка тестового приложения test-ui-megahiddensuffix.ptcloud.ru
- [ ] Определить границу control plane / border / agent

## Auth & Session
- [ ] JWT: alg, подпись, TTL, scope, ротация refresh
- [ ] Logout: инвалидация access/refresh
- [ ] Password change: инвалидация сессий
- [ ] Session fixation, кража cookie

## Tenant isolation
- [ ] Доступ к чужому tenant/customer/folder/domain
- [ ] Чтение чужих отчётов/инцидентов/рекомендаций
- [ ] IDOR по UUID/folder/domain

## Policy management
- [ ] Изменение/отключение/откат/навязывание политики чужому тенанту
- [ ] Доставка вредоносной конфигурации в клиентский контур

## Injection
- [ ] SQL/NoSQL/LDAP/template/command в настройках/поиске/фильтрах/экспорте
- [ ] Импорт правил/отчётов/конфигов/сертификатов/ключей

## XSS
- [ ] Stored в консоли (правила, отчёты, названия тенантов)

## SSRF
- [ ] Консоль управления / API / control plane

## Log injection
- [ ] Скрытие атаки, смена severity, привязка к чужому клиенту/домену

## AF bypass
- [ ] HTTP-парсинг: path normalization, mixed case, null bytes, uncommon separators
- [ ] Encoding: URL, Unicode, double, mixed
- [ ] JSON/XML/multipart/GraphQL/REST/SOAP/file upload/compressed/chunked/WebSocket/gRPC/HTTP/2
- [ ] TLS/HTTPS inspection
- [ ] Mismatch: атака дошла, а в консоли «заблокировано»/нет события

## Agent vulns (только тестовый tenant)
- [ ] DoS-safe PoC: рестарт, зависание, утечка ресурсов
- [ ] Утечка данных клиента (трафик, cookies, токены, ключи, конфиги, логи, topology)
- [ ] RCE/escape/privilege/read secrets/pivot — безопасный PoC

## RCE / sandbox
- [ ] Десериализация, escape, чтение секретов

## Secrets
- [ ] Телеметрия, debug endpoints, публичные buckets/registries/artifact storage
