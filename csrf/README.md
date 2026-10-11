# CSRF — Cross-Site Request Forgery

Подделка межсайтовых запросов: заставляем браузер жертвы отправить запрос от её имени.

## Лабы PortSwigger

- [Lab 01: CSRF vulnerability with no defenses](./lab-01-no-defenses.md) ✅

## Прогресс: 1/8

## Ключевые концепции

- Атака работает, потому что браузер **автоматически** прикладывает куки жертвы к запросу.
- Защита: CSRF-токен, проверка Origin/Referer, SameSite-куки.
