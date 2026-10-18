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

## Разведка и первые результаты
- Собран трафик через Burp Suite.
- Проверены методы `getOwnerStats` и `video.get` — оба требуют строгой авторизации (`error_code: 5`), IDOR не подтвержден.
- Обнаружены эндпоинты управления Live-стримами (`PUT /v8/channel/...`).

## План работ
1. Парсинг JS-бандлов (LinkFinder) для поиска скрытых API.
2. Поиск IDOR в Live-стримах и старом PHP-коде (`al_video.php`).
3. Тестирование Race Condition на метриках просмотров.

---
*Примечание: Все материалы публичны. Согласно правилам программы, никакие приватные данные, куки или токены не публикуются. Использовался только ручной тест в рамках скоупа.*
