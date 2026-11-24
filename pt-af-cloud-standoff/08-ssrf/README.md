# SSRF — PT AF Cloud

## Что ищем
SSRF в функциях консоли управления, API или control plane PT Cloud AF.

## Где искать
- Проверка URL / домена при добавлении защищаемого ресурса
- Webhook-уведомления (email / Slack / Telegram / custom)
- Импорт правил по URL
- Проверка сертификата (fetch chain, OCSP, CRL)
- Превью ссылок в инцидентах / отчётах
- Интеграции с внешними сервисами (callback, healthcheck)
- GraphQL: аргументы `url`, `endpoint`, `callback`
- PDF / отчёт generation (если рендерится из URL)

## Цели SSRF
- **Внутренние сервисы PT Cloud AF:** `http://127.0.0.1:8080`, `http://control-plane:8080`, `http://border:9090`
- **Metadata:** `http://169.254.169.254/latest/meta-data/` (если в облаке)
- **Внутренняя сеть:** `http://10.0.0.1/`, `http://192.168.0.1/`
- **Файлы:** `file:///etc/hostname`, `gopher://`, `dict://`
- **Кросс-tenant:** запрос к API другого tenant через внутренний адрес

## Обходы allow-list
```
http://evil.com@127.0.0.1/
http://127.0.0.1#@evil.com/
http://127.0.0.1.nip.io/
http://2130706433/       # decimal
http://0x7f.0.0.1/       # hex
http://127.1/            # short
http://[::1]/            # IPv6
DNS rebinding (свой DNS → 127.0.0.1)
Редирект с разрешённого домена
```

## Инструменты
- Burp Collaborator / interactsh
- SSRFmap
- Gopherus

## Чек-лист
- [ ] Найти все URL-параметры (webhook, import, preview, cert-check)
- [ ] Подставить Collaborator → увидеть запрос
- [ ] Проверить `http://169.254.169.254/latest/meta-data/` (только PoC)
- [ ] Проверить `file:///etc/hostname`
- [ ] Проверить обходы allow-list
- [ ] Проверить доступ к control plane / border из консоли
- [ ] Проверить кросс-tenant через внутренний API

## Не делать
- Не атаковать инфраструктуру клиентов
- Не пытаться использовать IAM-токены
- В PoC — только подтверждение (1 запрос к metadata)
