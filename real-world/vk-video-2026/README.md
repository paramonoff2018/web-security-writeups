# VK Видео — Bug Bounty Engagement

**Платформа:** BI.ZONE Bug Bounty
**Программа:** VK Видео (Tier 1: vkvideo.ru, m.vkvideo.ru, api.vkvideo.ru)
**Период:** Октябрь 2026
**Хантер:** [@paramonoff2018](https://github.com/paramonoff2018)

## Стек приложения
- **Frontend:** Svelte, VKUI
- **Backend:** PHP, KPHP
- **API:** `api.vkvideo.ru` (RPC-подобная архитектура `method/*`), `api.live.vkvideo.ru`
- **CMS:** Joomla (на отдельных частях)

## Ход исследования (Recon & Testing)

### 1. Сбор трафика и Scope
- Настроен Burp Suite (Scope: `*.vkvideo.ru`, Match&Replace: `X-Bug-Bounty`).
- Проанализирован трафик кабинета автора (`cabinet.vkvideo.ru`) и видеосервиса (`vkvideo.ru`).

### 2. Проверка API Методов
- **`statsVideoDashboard.getOwnerStats`**: При подмене `owner_id` на чужой канал возвращает `error_code: 5` (User authorization failed). Защита работает корректно.
- **`video.get`**: При попытке запросить публичное видео через ручной запрос возвращает `error_code: 5`. Метод требует авторизации.
- **Вывод:** Классические методы VK API защищены проверкой прав на уровне шлюза.

### 3. Анализ JavaScript (Recon)
С помощью инструмента **LinkFinder** был проведен статический анализ JS-бандлов (скачаны с `st1-28.vkvideo.ru`).
- В файле `ads_light` (рекламный модуль) обнаружен внутренний API: `https://akashi.vk-portal.net/api/v1/web`. Прямой запрос возвращает `403 Forbidden`.
- Также найдены эндпоинты для сбора метрик (`/api/perf/upload`, `/api/crash/uploadBatch`).

## План дальнейших работ
1. Тестирование Legacy PHP-эндпоинтов (`/al_video.php`, `/usefull.php`) на предмет IDOR и Business Logic.
2. Проверка `PUT /v8/channel/...` на `api.live.vkvideo.ru` (Broken Access Control / захват чужого стрима).

---
*Примечание: Все материалы публичны. Согласно правилам программы, никакие приватные данные, куки или токены не публикуются. Использовался только ручной тест в рамках скоупа.*
