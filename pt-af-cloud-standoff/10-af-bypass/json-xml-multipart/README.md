# AF Bypass — JSON / XML / Multipart / GraphQL / gRPC

## Что ищем
Обход inspection для структурированных форматов: JSON, XML, multipart, GraphQL, REST, SOAP, file upload, compressed bodies, chunked transfer, WebSocket, gRPC, HTTP/2.

## ⚠️ Главное правило PT
Сам факт прохождения payload'а через AF **не считается обходом**, если backend не исполнил атаку.

## JSON
- **Вложенные структуры:** `{"a":{"b":{"c":"<script>"}}}` — если AF смотрит только на верхний уровень
- **Unicode escape:** `{"x":"\u003cscript\u003e"}` — AF не декодирует `\u`
- **Дублирующиеся ключи:** `{"x":"safe","x":"<script>"}` — backend берёт последний, AF — первый
- **Большие числа / NaN / Infinity:** `{"x":1e10000}`
- **Content-Type confusion:** `Content-Type: application/json` + body `x=<script>` (AF парсит как JSON — падает; backend — как form)
- **JSONP:** `?callback=<script>`

## XML
- **XXE:** `<!ENTITY xxe SYSTEM "file:///etc/passwd">` (см. `05-injection/xxe`, если появится)
- **CDATA:** `<![CDATA[<script>]]>`
- **Namespace:** `<x:script xmlns:x="...">`
- **XInclude:** `<xi:include href="file:///etc/passwd"/>` (если DOCTYPE заблокирован)
- **DTD:** внешний DTD через `SYSTEM`
- **UTF-16 XML:** `<?xml version="1.0" encoding="UTF-16"?>`
- **Billion Laughs:** **ЗАПРЕЩЕНО** (DoS)

## Multipart
- **Границы:** `--boundary` с `\r\n` vs `\n`
- **Вложенные multipart:** `multipart/mixed` внутри `multipart/form-data`
- **Filename injection:** `filename="x.php\0.jpg"`, `filename="../../etc/passwd"`
- **Content-Type на part:** `Content-Type: text/html` для загруженного файла
- **Много частей:** AF смотрит первые N, backend — все

## GraphQL
- **Aliases:** `query { a: __typename b: __typename ... }` (AF видит 1 поле, backend — N)
- **Fragments:** скрытие payload'а во фрагменте
- **Introspection:** `__schema`, `__type` — если AF блокирует, обойти через aliases
- **Batching:** `[{...},{...}]` — AF смотрит первый, backend — все
- **Переменные:** payload в `variables`, не в `query`
- **Content-Type:** `application/graphql` vs `application/json`

## gRPC / HTTP/2 / WebSocket
- **gRPC:** бинарный protobuf — AF может не парсить
- **HTTP/2:** HPACK-сжатие заголовков, `:path` vs `:authority`
- **WebSocket:** upgrade → AF перестаёт инспектировать (проверить!)
- **HTTP/2 → HTTP/1 downgrade:** на границе AF

## Compressed / Chunked
- **gzip / deflate / br:** payload сжат, AF не распаковывает
- **Chunked:** payload разбит на чанки, AF не собирает
- **Chunked + gzip:** комбинация

## Инструменты
- Burp (ручное)
- GraphQL Voyager / InQL
- grpcurl
- websocat
- Кастомные скрипты для multipart / chunked

## Чек-лист
- [ ] JSON: вложенность, `\u`, дубликаты ключей, Content-Type confusion
- [ ] XML: CDATA, namespace, XInclude, UTF-16
- [ ] Multipart: границы, вложенность, filename injection
- [ ] GraphQL: aliases, fragments, batching, variables
- [ ] gRPC / HTTP/2 / WebSocket
- [ ] gzip / deflate / br / chunked
- [ ] **Для каждого прошедшего — доказать, что backend исполнил**
- [ ] Проверить, что AF не залогировал как атаку

## Не делать
- Не использовать Billion Laughs / quadratic blowup (DoS)
- Не считать «прошло через AF» = «обход»
