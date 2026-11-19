# CONTINUE — точка входа для нового чата / агента

> Этот файл читается первым при возобновлении работы. Он — внешняя память проекта.
> Обновляется после каждой сессии (лабы, write-up, коммита).

## Что это за репозиторий

Разборы **PortSwigger Web Security Academy** + подготовка к **real-world bug bounty** (Avito / Bi.Zone, PT AF Cloud / Standoff 365).

## Текущее состояние

- **PortSwigger:** 16 / 129
- **XSS:** 1 / 30
- **Последний коммит:** `5563609` — `docs: fix broken Structure section in README`
- **Активные программы:** `avito-bizone/`, `pt-af-cloud-standoff/` (обе наполнены README по темам)

## Структура

- `csrf/`, `sqli/`, `xss/`, `access-control/`, `authentication/`, `api-testing/`, `web-llm-attacks/`, `web-cache-deception/`, `path-traversal/`, `nosql-injection/`, `race-conditions/`, `xxe/` — темы PortSwigger
- `avito-bizone/` — программа Avito (Bi.Zone): 12 README по темам + `_program/` + `_templates/`
- `pt-af-cloud-standoff/` — программа PT AF Cloud (Standoff 365): 22 README + `_program/` + `_templates/`
- `real-world/` — реальные bug bounty
- `templates/` — шаблоны write-up
- `_shared/` — общие шаблоны (report / poc / checklist)
- `CONTINUE.md` — этот файл

## Конвенции

- **Текст в write-up — на русском.** Названия (PortSwigger, Apprentice, Reflected XSS), код, payload'ы, HTTP-запросы — **как есть на английском**.
- **Один write-up = одна папка:** `<тема>/<slug>/README.md` (например `xss/reflected-xss-html-nothing-encoded/README.md`).
- **После каждой лабы:** обновить таблицу в `README.md` (тема +1, Всего +1), обновить строку «Последнее решённое», сделать коммит.
- **Сообщения коммитов:** `docs(<тема>): add <slug> write-up` / `docs: fix ...` / `chore: ...`.
- **Предупреждения `LF will be replaced by CRLF`** — норма на Windows (`core.autocrlf=true`), игнорировать.
- **Секреты не коммитить:** API-ключи, токены, `.env` — только через env-переменные окружения.

## Следующий шаг

**Лаба #2 по XSS:** *Reflected XSS into HTML context with most tags and attributes blocked* (Apprentice).
Slug-кандидат: `xss/reflected-xss-most-tags-blocked/README.md`.
Что нового: обход allow-list тегов/атрибутов через `<body onresize=print()>` + iframe, `onresize` срабатывает при ресайзе.

## Как продолжить в новом чате (bootstrap-промпт)

Скопируй в первый запрос:

```
Репозиторий: https://github.com/paramonoff2018/web-security-writeups
Прочитай CONTINUE.md в корне — там состояние, конвенции и следующий шаг.
Работаем пошагово: один блок PowerShell → я запускаю → показываю вывод → следующий блок.
После каждой лабы — коммит и push. Текст write-up на русском, код/payload — как есть.
Продолжаем с лабы #2 XSS (most tags and attributes blocked).
```

## Заметки по API / VS Codium

- Расширения (Continue, Cline, Roo Code) читают файлы воркспейса — упомяни `CONTINUE.md` в контексте или добавь его в custom instructions расширения.
- **Не хардкодь API-ключ в файлах репозитория** — используй `DEEPSEEK_API_KEY` в окружении или в настройках расширения (локально, вне git).
- Если работаешь через голый API (curl/Python) — передавай `CONTINUE.md` в system-промпте или первым user-сообщением.

## Что НЕ делать

- Не переписывать `_shared/` шаблоны без нужды — они переиспользуются обеими программами.
- Не смешивать коммиты «write-up лабы» и «косметика README» — отдельные коммиты (как `84c29b2` vs `5563609`).
- Не удалять `.gitkeep` в пустых папках программ — git перестанет видеть дерево.
