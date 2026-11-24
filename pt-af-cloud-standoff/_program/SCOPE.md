# PT AF Cloud — SCOPE

## In-scope
- `*.ptcloud.ru` и поддомены
- Агент для фильтрации трафика: https://storage.ptsecurity.com/d/9071a220b91d4371809f/
- Защищаемые тестовые приложения: https://test-ui-megahiddensuffix.ptcloud.ru/

## Вне scope (выплата не гарантируется, но можно отправить)
- Уязвимости за пределами scope, но прямо влияющие на PT Cloud AF или безопасность клиентов AF — рассматриваются, выплата не гарантируется.

## Out-of-scope
- Строки/payload'ы, имитирующие атаку, но не валидные/исполняемые для целевого парсера/языка/протокола — **без подтверждённой эксплуатации**.
- Сам факт прохождения конструкции через AF ≠ обход.

## Что искать (категории)
- Аутентификация/авторизация, эскалация, доступ к чужим tenant/folder/domain
- Session capture/fixation, утечки cookies/access/refresh, отсутствие ротации
- Stored XSS в консоли
- SQL/NoSQL/LDAP/template/command injection
- Загрузка файлов/импорт правил/конфигов/сертификатов
- Управление политиками (навязать/откатить/отключить чужому тенанту)
- RCE/escape/sandbox/deserialization
- Log injection/forging
- Утечка secrets через телеметрию/debug/buckets
- SSRF в консоли/API/control plane
- AF bypass (парсинг, кодировки, JSON/XML/multipart/GraphQL, TLS, mismatch detection)
- Agent vulns (DoS-safe PoC, утечки, RCE, pivot — только в тестовом тенанте)
