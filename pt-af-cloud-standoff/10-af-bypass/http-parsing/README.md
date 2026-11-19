# AF Bypass — HTTP Parsing

## Что ищем
Обход блокирующих правил AF через особенности HTTP-парсинга: path normalization, mixed case, null bytes, uncommon separators.

## ⚠️ Главное правило PT
> Тестовые строки и payload'ы, имитирующие атаку, **но не являющиеся валидными и исполняемыми** с точки зрения целевого языка/протокола/парсера — **без подтверждения фактической эксплуатации и влияния на тестовое приложение** — **не считаются** обходом.
>
> **Сам факт прохождения такой конструкции через PT Cloud AF ≠ обход защиты.**

То есть: `GET /..%00/admin` вернул 200 от AF — это **не находка**, если backend не интерпретирует это как `/admin`. Нужно доказать, что **backend выполнил атаку**, а AF — **не заблокировал**.

## Векторы
- **Path normalization:**
  - `/admin` → `/./admin`, `/foo/../admin`, `//admin`, `/admin/`, `/admin/.`
  - `%2e%2e`, `%2e.`, `.%2e`, `%252e%252e` (double encoding)
  - `..;/`, `/..;/`, `/.;/`, `/..%2f`
  - Unicode: `／` (fullwidth solidus), `∕` (division slash)
- **Mixed case:**
  - `/ADMIN`, `/Admin`, `/aDmIn`
  - `/admin%00`, `/admin%20`
- **Null bytes:**
  - `/admin%00.jpg`, `/admin%00.html`
  - `/etc/passwd%00.png`
- **Uncommon separators:**
  - `;` (matrix params): `/admin;foo=bar`
  - `,` : `/admin,foo`
  - `|`, `\`, `^`
- **Backslash:** `\admin`, `/..\admin`
- **Trailing / leading:**
  - `/admin/` vs `/admin` vs `/admin//`
  - ` /admin`, `\t/admin`, `/admin\r\n`
- **HTTP request smuggling (если применимо):**
  - CL.TE, TE.CL, TE.TE (только если есть цепочка front ↔ back)
- **Метод-подмена:**
  - `GET /admin HTTP/1.1` vs `POST /admin` vs `HEAD /admin`
  - `X-HTTP-Method-Override: GET`

## Как валидировать (обязательно!)
1. **Доказать, что backend исполнил:** ответ тестового приложения содержит результат атаки (например, `id` вернул `uid=...`, `/admin` вернул админку).
2. **Доказать, что AF пропустил:** в событиях AF этот запрос **не заблокирован** и **не помечен как атака**.
3. **Mismatch (отдельно, см. detection-mismatch):** AF в консоли пишет «заблокировано», а запрос реально дошёл до backend.

## Инструменты
- Burp Repeater (ручной перебор)
- ffuf с кастомным wordlist (path normalization)
- `curl --path-as-is` (важно: curl по умолчанию нормализует путь)
- interactsh (OOB для SSRF/RCE)

## Чек-лист
- [ ] Собрать список защищаемых эндпоинтов (admin, internal, /etc/passwd)
- [ ] Для каждого — прогнать path normalization вариации
- [ ] Для каждого — прогнать mixed case, null bytes, uncommon separators
- [ ] **Для каждой прошедшей конструкции — доказать, что backend её исполнил**
- [ ] Проверить, что AF в событиях **не заблокировал** этот запрос
- [ ] Если AF заблокировал, но backend исполнил — это отдельная находка (detection-mismatch)

## Не делать
- Не считать «прошло через AF» = «обход»
- Не присылать отчёты без PoC на backend
- Не использовать non-executable payload'ы (это прямая цитата из out-of-scope)
