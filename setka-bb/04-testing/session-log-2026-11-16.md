# Сессия 2026-11-16 (Понедельник) - WAF, ATO & Logic Tests

## 1. Stored XSS (Статус профиля, Посты)
- Payload: <img src=x onerror=alert(document.domain)>
- Результат: WAF (DDoS-Guard) блокирует запрос, возвращая 423 Locked. В статусе остается старое значение.
- Вывод: Вектор XSS в текстовых полях закрыт WAF.

## 2. File Upload (Аватарка, SVG)
- Эндпоинт: PUT /uploads/files
- Payload: Попытка загрузки .svg с тегом <script>.
- Результат: WAF возвращает 423 Locked. Попытка обхода через смену Content-Type на image/png также заблокирована.
- Вывод: Загрузка вредоносных файлов заблокирована WAF.

## 3. CSRF на удаление аккаунта
- Эндпоинт: POST /profile/deletion
- Тест: HTML-форма на локальном файле.
- Результат: Аккаунт не удалился (защита через SameSite cookies / Origin).
- Вывод: CSRF защита работает.

## 4. OTP & Rate Limit (Авторизация по SMS)
- Эндпоинт: POST /login/otp/{uuid}/verify
- Тест: Отправка 10 запросов с неверным кодом 111111.
- Результат: Сервер вернул ошибку "слишком много попыток". 
- Вывод: Rate Limit на OTP работает, брутфорс закрыт.

## Итог сессии
Проверено 4 вектора (XSS, File Upload, CSRF, OTP Bruteforce). 
Обнаружено, что WAF и Rate Limit настроены надежно. Подтвержденных High/Medium уязвимостей нет.
