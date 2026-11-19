# Auth & Session — Avito

## Что ищем
Broken Authentication and Session Management (из перечня Avito).

## Векторы
- **JWT:** alg=none, слабый секрет, отсутствие проверки подписи, kid/jku injection, отсутствие exp
- **OAuth:** redirect_uri без валидации, отсутствие state, scope escalation, implicit flow
- **Session:** фиксация, отсутствие ротации после логина, невалидация при logout, невалидация при смене пароля
- **Password reset:** утечка токена, предсказуемость, token reuse, host header injection
- **MFA / 2FA:** обход, отсутствие rate limit, OTP brute
- **API-токены:** долгоживущие, без scope, утечки в мобильных приложениях

## Out-of-scope (НЕ репортить)
- Session hijacking, session timeout
- Отсутствие флагов cookie (HttpOnly / Secure / SameSite)
- Парольные политики
- Отсутствие rate limit без существенно более эффективного метода

## Инструменты
- jwt_tool, jwt-hack
- Autorize (Burp), AuthMatrix
- Postman/Insomnia для API-флоу

## Чек-лист
- [ ] Логин / регистрация: обходы, дублирование email/phone
- [ ] JWT: декодировать, попробовать alg=none и слабый секрет
- [ ] OAuth-флоу: подменить redirect_uri, убрать state
- [ ] Сброс пароля: анализ токена, повторное использование
- [ ] Logout: проверить инвалидацию access/refresh
- [ ] Смена пароля: проверить инвалидацию сессий

## Не делать
- Не брутить чужие аккаунты
- Не тестировать на реальных пользователях
