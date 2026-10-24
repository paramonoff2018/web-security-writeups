# Карта векторов — VK Видео

**Легенда:** [ ] не начат | [~] в работе | [x] пройден | [!] БАГ

## A. Recon
- [x] Wappalyzer (Svelte, PHP, Joomla, Sentry)
- [x] LinkFinder (нашли `akashi.vk-portal.net`, `pay_url`)
- [x] Проверка Swagger/OpenAPI (404 на всех путях)
- [ ] arjun (поиск скрытых параметров) — *на будущее*

## B. Live Стримы (api.live.vkvideo.ru)
- [x] `PUT /v8/channel/{name}/manage/description` — 400 Bad Request (защищено)
- [x] `GET /v8/channel/{name}/notification_settings` — 200 OK (только дефолтные значения)
- [x] `GET /v8/channel/{name}` — 200 OK (только публичные данные)
- [x] Race Condition на `pay_url` — [!] БАГ (закрыт как Информативный, риск принят)
- [ ] IDOR в чате (`/chat/settings`, `/chat/user`)
- [ ] Захват стрима (`PUT /v8/channel/{name}/stream/{id}`)

## C. API Методы (api.vkvideo.ru)
- [x] `statsVideoDashboard.getOwnerStats` — 401 (защищено)
- [x] `video.get` — 401/Пустой массив (защищено)
- [ ] `catalog.getVideo` — IDOR (подстановка скрытого video_id)
- [ ] `messages.getConversationsById` — IDOR (чужие переписки)
- [ ] `account.getInfo` — Excessive Data Exposure

## D. Legacy PHP (vkvideo.ru)
- [ ] `al_video.php` — IDOR / SQLi / LFI
- [ ] `usefull.php` — Logic Flaws

## E. ИИ / Prompt Injection
- [x] Поиск в Студии VK Видео — кнопок ИИ не найдено (вектор закрыт)
