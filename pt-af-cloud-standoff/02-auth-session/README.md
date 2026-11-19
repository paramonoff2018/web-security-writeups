# Auth & Session — PT AF Cloud

## Что ищем
Нарушения аутентификации/авторизации, сессии, токены — в консоли управления, API, control plane.

## Векторы
- **JWT:**
  - alg=none / alg confusion (RS256 → HS256)
  - Слабый секрет (hashcat)
  - `kid`/`jku`/`x5u` injection
  - Отсутствие проверки `exp`, `aud`, `iss`
  - TTL слишком большой, отсутствие ротации
- **Refresh-токены:**
  - Не инвалидируются после logout
  - Не инвалидируются после смены пароля
  - Отсутствие ротации (reuse detection)
  - Scope escalation через refresh
- **Session:**
  - Фиксация (session fixation)
  - Кража cookie (только если есть XSS — см. 07-xss)
  - Повторное использование access после logout
- **OAuth / SSO:**
  - `redirect_uri` без валидации
  - Отсутствие `state` (CSRF)
  - `scope` escalation
- **MFA:**
  - Обход, отсутствие rate limit (но без brute force!)

## Out-of-scope
- Отсутствие security headers / флагов cookie
- Session hijacking, session timeout (правила PT)
- Отсутствие rate limit без существенно более эффективного метода

## Инструменты
- jwt_tool, jwt-hack, hashcat
- Burp Autorize
- Postman

## Чек-лист
- [ ] Декодировать JWT из консоли, проверить claims
- [ ] Попробовать alg=none / alg confusion
- [ ] Попробовать слабый секрет (rockyou)
- [ ] Проверить logout: access/refresh невалидны?
- [ ] Проверить смену пароля: все сессии инвалидированы?
- [ ] Проверить ротацию refresh (reuse → ошибка?)
- [ ] Проверить OAuth: redirect_uri, state, scope
- [ ] Проверить MFA-флоу на обход

## Не делать
- Не брутить чужие учётки (mass brute force — запрещено)
- Не выполнять действия от имени другого пользователя за пределами PoC
- В PoC — только на своём тестовом аккаунте
