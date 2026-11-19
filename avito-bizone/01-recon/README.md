# Recon — Avito

## Scope
**critical:** android/ios apps, api.avito.ru, m.avito.ru, payments.avito.ru, www.avito.ru
**high:** *.hrbt.ru, *.hmsg.me, hrmka.ru, *.haraba.ru, *.maxposter.ru, *.hrmessenger.com, *.autoteka.ru, *.avito.ru

## Что собираем
- Поддомены по всем scope-доменам
- Endpoints из мобильных приложений (APK / IPA)
- API: REST, GraphQL, gRPC, WebSocket
- CDN, S3-бакеты, статика
- Технологический стек (Wappalyzer, headers, ошибки)

## Инструменты
- subfinder, amass, assetfinder
- httpx, httprobe
- katana, gau, waybackurls, paramspider
- jadx, apktool, MobSF (для APK/IPA)
- nuclei, ffuf

## Куда смотреть в первую очередь
- **HR-системы** (*.hrbt.ru, *.hmsg.me, hrmka.ru, *.hrmessenger.com) — часто менее закалены, чем основной прод
- **autoteka.ru** — VIN-номера, авто-данные
- **haraba.ru, maxposter.ru** — интеграции с внешними партнёрами
- **мобильные приложения** — жёстко зашитые эндпоинты, ключи, feature-flags

## Осторожно
- Не сканировать платёжные шлюзы и сайты-партнёры
- Соблюдать rate limit, никакого DoS
- Не трогать чужие аккаунты

## Чек-лист
- [ ] subfinder по всем scope-доменам
- [ ] httpx -title -tech-detect по найденным
- [ ] Скачать APK + IPA, распаковать, вытащить строки/URL
- [ ] Собрать JS-бандлы, поискать API-эндпоинты
- [ ] Сохранить результаты в _notes/
