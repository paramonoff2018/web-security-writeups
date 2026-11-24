# AF Bypass — Encoding & Normalization

## Что ищем
Обход блокирующих правил AF через URL encoding, Unicode normalization, double encoding, mixed case.

## ⚠️ Главное правило PT
Сам факт прохождения payload'а через AF **не считается обходом**, если backend не исполнил атаку. См. `http-parsing/README.md`.

## Векторы
- **URL encoding:**
  - `%3Cscript%3E` вместо `<script>`
  - `%253Cscript%253E` (double encoding)
  - `%25253C` (triple)
  - Частичное кодирование: `<scr%69pt>`
- **Unicode normalization:**
  - Fullwidth: `＜script＞`, `ａｄｍｉｎ`
  - Cyrillic homoglyphs: `аdmin` (кириллица `а`)
  - NFKC / NFKD: `ﬁ` → `fi`, `①` → `1`
  - Overlong UTF-8: `%c0%af` → `/`
  - UTF-16 / UTF-7: `+ADw-script+AD4-` (UTF-7 XSS)
- **Case:**
  - `<ScRiPt>`, `<IMG SRC=x onerror=...>`
  - Заголовки: `Content-Type: text/html` vs `TEXT/HTML`
- **Mixed encoding:**
  - `%3Cscript%3E` + `<svg/onload=...>`
  - Часть payload'а в URL, часть в body
- **HTML-entities:**
  - `&#x3c;script&#x3e;`, `&lt;script&gt;`
- **Base64 / hex в параметрах:**
  - `?data=PHNjcmlwdD4=` (если backend декодирует)
- **Chunked / gzip / deflate:**
  - `Content-Encoding: gzip` + сжатый payload
  - `Transfer-Encoding: chunked` + разбитый payload

## Как валидировать
1. **Backend исполнил:** XSS сработал в браузере, SQLi вернул данные, RCE вернул `id`, path traversal вернул `/etc/passwd`.
2. **AF не заблокировал:** в событиях AF запрос не помечен как атака.
3. **AF не декодировал payload** (или декодировал неверно) — это и есть суть обхода.

## Инструменты
- Burp (ручное кодирование)
- `ffuf` с payload-кодированием (`-e`)
- `curl` с `--path-as-is`
- Кастомные скрипты для NFKC/NFKD

## Чек-лист
- [ ] Собрать список WAF-правил (по сигнатурам: `<script`, `union select`, `../`)
- [ ] Для каждого сигнатурного payload'а — прогнать URL encoding
- [ ] Прогнать double encoding
- [ ] Прогнать Unicode normalization (fullwidth, homoglyphs, NFKC)
- [ ] Прогнать mixed case
- [ ] Прогнать UTF-7 / UTF-16
- [ ] Прогнать gzip / chunked
- [ ] **Для каждого прошедшего — доказать, что backend исполнил**
- [ ] Проверить, что AF не залогировал как атаку

## Не делать
- Не считать «прошло через AF» = «обход»
- Не присылать non-executable payload'ы
- Не использовать DoS-кодировки (quadratic blowup)
