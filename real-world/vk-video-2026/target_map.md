## 5. КАРТА ЦЕЛЕЙ И ПРИОРИТЕТЫ (по трафику)

### 🎯 Приоритет 1: BOLA / IDOR (Самый высокий шанс + Высокая выплата)
*Везде, где есть ID или UUID, мы пробуем подставить ID второго аккаунта.*

**A. Статистика и Монетизация (api.vkvideo.ru)**
- `POST /method/statsVideoDashboard.getOwnerStats` (Вызывается часто, шлет JSON с ID канала)
- `POST /method/statsVideoDashboard.getMonetizationSettings` (Настройки монетизации чужого канала = 💰)
- `POST /method/statsVideoDashboard.getSections`
- `POST /method/account.getInfo` (Может отдавать PII чужого юзера)
- `POST /method/messages.getConversationsById` (Чужие переписки = Critical)

**B. Управление контентом (api.live.vkvideo.ru)**
- `PUT /v8/channel/{channel_name}/stream/{stream_id}` (Изменение параметров чужого стрима!)
- `GET /v1/channel/{channel_name}/stream/slot/...`
- `POST /method/video.bulkEditGetTasks` (Задачи на массовое редактирование)
- `POST /method/video.getOwnerComments` (Комментарии, возможно скрытые)

**C. Видео и Приватность**
- `POST /method/video.getPrivacyDictionary` (Какие настройки приватности доступны?)
- `POST /method/catalog.getVideo` (Получение инфы о видео по ID)

### 🎯 Приоритет 2: Business Logic / Race Condition (Гонка)
- `POST /method/stats.trackEvents` (Накрутка метрик)
- `POST /method/video.viewStarted` и `POST /method/video.trackPlayerEvents` (Накрутка просмотров через Race Condition - отправка 10 запросов одновременно)

### 🎯 Приоритет 3: Legacy PHP (cabinet.vkvideo.ru / vkvideo.ru)
*Старый код часто содержит дыры.*
- `POST /al_video.php?act=web_token`
- `POST /al_video.php` (Основной старый метод)
- `POST /usefull.php`
- `POST /politics`

---

### 🚀 ПЛАН АТАКИ НА СЕГОДНЯ (Step-by-Step)

**Шаг 1: Разбираем getOwnerStats**
1. В Burp найди запрос `POST /method/statsVideoDashboard.getOwnerStats`.
2. Отправь его в Repeater.
3. Посмотри вкладку **Request Body** (тело запроса). Скорее всего, там есть JSON вроде `{"channel_id": 123, ...}` или параметры `owner_id`.
4. Найди `owner_id` **своего второго аккаунта** (зайди под ним и посмотри такой же запрос).
5. Подставь ID второго аккаунта в запрос от первого. Нажми Send.
6. **Если вернулась статистика чужого канала -> ЭТО БАГ (IDOR).**

**Шаг 2: Разбираем live-стримы**
1. Найди запрос `PUT /v8/channel/burushkaplay/stream/70b6...`.
2. Это запрос на **обновление** стрима.
3. Отправь в Repeater. Попробуй поменять `burushkaplay` на имя канала другого стримера (найди его на сайте).
4. Если сервер ответит `200 OK` и изменит что-то у него -> **КРИТИЧЕСКИЙ БАГ**.

## 6. РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ (18.10.2026)

### Тест 1: statsVideoDashboard.getOwnerStats
- **Действие:** Заменили `owner_id` на `-206304696` (чужой канал).
- **Результат:** `HTTP/2 200 OK`, но в теле `{"error":{"error_code":5,"error_msg":"User authorization failed"}}`.
- **Вывод:** Защита работает. Сервер проверяет права на просмотр статистики. Не баг.

### Тест 2: video.get (ручной запрос)
- **Действие:** Попытались запросить данные публичного видео `-206304696_456240102` через метод `video.get`.
- **Результат:** `HTTP/2 200 OK`, в теле `error_code: 5 (User authorization failed)`.
- **Вывод:** Метод требует специфичных прав токена (возможно, токен приложения). Прямой вызов через `api.vkvideo.ru` закрыт.

### Текущий статус
- Найдено API: `api.vkvideo.ru`, `api.live.vkvideo.ru`.
- Найдены эндпоинты для управления стримами (`PUT /v8/channel/...`) — **следующий приоритет**.
- Legacy PHP (`al_video.php`) — **второй приоритет**.

### НЕ забыть
- Провести атаку в стиле Гонки с микрозадержками на авторизацию и другие векторы.

## 7. РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ (19.10.2026)

### Тест 3: video.get (ручной запрос)
- **Запрос:** `POST /method/video.get` с ID публичного видео.
- **Ответ:** `200 OK`, `error_code: 5` (User authorization failed).
- **Вывод:** Защищено. Требует специфичный токен.

### Тест 4: Live-стримы (PUT)
- **Статус:** В работе. Найдены эндпоинты `PUT /v8/channel/{name}/stream/{id}`.
- **Цель:** Проверить изменение чужого стрима.

### Тест 5: Legacy PHP
- **Статус:** В работе. Найдены `POST /al_video.php`, `POST /usefull.php`.
- **Цель:** IDOR / SQLi / Logic Flaws.

---

## 8. RECON: JS-АНАЛИЗ (LinkFinder)

- **Файл:** `ads_light.2aeb0931.js` (449 КБ)
- **Найдено:** 
  - `https://akashi.vk-portal.net/api/v1/web` (внутренний рекламный API, 403 Forbidden при прямом запросе).
  - `/api/crash/uploadBatch`, `/api/perf/upload`, `/api/crash/trackSession` (Sentry/метрики, не баг).
- **Файлы `notifier.js` и `ui_common.js`:** скрытых API-путей не найдено (динамическая сборка).

## 9. ПОТЕНЦИАЛЬНЫЙ БАГ: Race Condition на создание платежной ссылки (pay_url)

**Дата:** 22.10.2026
**Эндпоинт:** `POST /v1/channel/kop3uhbl4/subscription/level/6880/gift/bank131/pay_url/`
**Платформа:** api.live.vkvideo.ru

### Суть
При отправке двух одинаковых запросов на создание ссылки для оплаты подарочной подписки сервер возвращает два разных `paymentId` и две разные ссылки на оплату. Отсутствует идемпотентность (дедупликация).

### PoC (доказательство)
- Запрос 1 → `paymentId: 235083947`, url: `...token=f256a6...`
- Запрос 2 → `paymentId: 235083948`, url: `...token=db2cd80a...`
- Оба ответа `HTTP/1.1 200 OK`.

### Потенциальный Impact
Пользователь может случайно создать несколько валидных платёжных ссылок на один товар. Это может привести к двойному списанию средств при повторном нажатии или ошибке сети.

### Статус: Готовим отчёт на BI.ZONE

## 11. 2026-10-24 (Сессия 2) — Swagger, IDOR, ИИ

### Проверено (закрыто, не баг)
1. **Swagger/OpenAPI:** `/swagger.json`, `/openapi.json` на `api.` и `api.live.` -> 404.
2. **IDOR GET (Live):** `notification_settings` (дефолт), `channel` (публичные данные) -> защищено.
3. **IDOR PUT (Live):** `manage/description` -> 400 Bad Request.
4. **IDOR (api.vkvideo.ru):** `video.get` с несуществующим ID -> пустой массив.
5. **ИИ:** В Студии кнопок генерации нет.

### Вывод
VK надежно защищает state-changing запросы на Live. Все IDOR-попытки возвращают 400/403 или публичные данные. 
