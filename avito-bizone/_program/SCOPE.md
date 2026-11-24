# Avito — SCOPE

## In-scope
| Актив | Критичность | Выплата |
|---|---|---|
| android / ios apps | critical | да |
| api.avito.ru | critical | да |
| m.avito.ru | critical | да |
| payments.avito.ru | critical | да |
| www.avito.ru | critical | да |
| *.hrbt.ru (HRM) | high | да |
| *.hmsg.me (HRM) | high | да |
| hrmka.ru (HRM) | high | да |
| *.haraba.ru (Haraba) | high | да |
| *.maxposter.ru (Maxposter) | high | да |
| *.hrmessenger.com (HRM) | high | да |
| *.autoteka.ru | high | да |
| *.avito.ru (все остальные) | high | да |

## Out-of-scope
- Сканеры без анализа и PoC
- Версии ПО без эксплуатации
- Отсутствие best practices без PoC
- Парольные политики
- Малое раскрытие информации
- Self-XSS
- SSL-недостатки
- Clickjacking
- Подмена контента без модификации HTML/CSS
- Уязвимости только в устаревших браузерах
- Session hijacking, session timeout
- Отсутствие security headers / флагов cookies
- Отсутствие SPF/DKIM/DMARC
- Перебор ID объявлений/пользователей
- Enumeration имён/e-mail
- Уже известные / внутренние находки
