# File Upload / Import — PT AF Cloud

## Что ищем
Уязвимости загрузки файлов, импорта правил, отчётов, конфигураций, сертификатов и ключей.

## Где искать
- Импорт правил AF (YAML / JSON / XML / proprietary)
- Импорт конфигураций (backup / restore)
- Загрузка сертификатов (TLS, client certs)
- Загрузка ключей (private keys, API keys)
- Импорт отчётов (PDF / CSV / JSON)
- Загрузка логотипа tenant / брендинга
- Импорт пользователей (CSV / LDAP dump)
- Импорт политик из другого tenant

## Векторы
- **Path traversal в имени файла:** `../../etc/cron.d/x`, `..\..\web\shell.jsp`
- **Обход расширений:** `.php.jpg`, `.jsp%00.png`, `.phtml`, `.phar`, `.htaccess`
- **Polyglot:** валидный JPG + PHP-код в EXIF / comment
- **XXE в XML-импорте** (см. 05-injection/xxe, если появится)
- **SSRF через URL-импорт** (см. 08-ssrf)
- **RCE через десериализацию** в импорте правил (см. 12-rce-sandbox)
- **Symlink / zip-slip:** zip с `../` внутри
- **Mass assignment в импорте:** подмена `tenant_id` в YAML/JSON
- **Перезапись чужих правил / политик** через импорт (см. 04-policy-management)

## Ограничения PT
- PoC — только безопасная запись (`/tmp/poc`), не `/etc/cron.d`
- Не заливать webshell с persistence
- Не перезаписывать чужие правила / политики
- Не выполнять destructive payload'ы

## Инструменты
- Burp + Upload Scanner
- zip-slip генераторы
- exiftool (polyglot)
- ysoserial / phpggc (если десериализация)

## Чек-лист
- [ ] Найти все точки загрузки (правила, конфиги, сертификаты, отчёты)
- [ ] Проверить path traversal в имени файла
- [ ] Проверить обход расширений
- [ ] Проверить polyglot (JPG + PHP)
- [ ] Проверить zip-slip
- [ ] Проверить импорт правил на mass assignment / RCE
- [ ] Проверить импорт сертификатов / ключей на path traversal
- [ ] Проверить импорт из чужого tenant (изоляция)

## Не делать
- Не заливать destructive / persistence payload'ы
- Не перезаписывать `/etc/`, cron, systemd
- В PoC — только запись в `/tmp` и чтение
