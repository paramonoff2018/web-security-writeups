# Secrets Leaks — PT AF Cloud

## Что ищем
Утечка чувствительных данных (secrets, tokens) через телеметрию, debug endpoints или иные механизмы отладки.

## Категории (из правил PT)
- Утечка secrets / tokens через телеметрию
- Утечка через debug endpoints
- Утечка через иные механизмы отладки

## Где искать
- **Debug endpoints:**
  - `/debug`, `/debug/pprof`, `/debug/vars`, `/actuator`, `/actuator/env`
  - `/metrics`, `/health`, `/status` (с лишними полями)
  - `/api/v1/debug`, `/internal/debug`
- **Телеметрия:**
  - `/telemetry`, `/analytics`, `/events`, `/logs`
  - Заголовки ответа (Server, X-Powered-By, X-Debug)
- **Публичные buckets / registries / artifact storage:**
  - S3, GCS, Azure Blob, Docker Hub, Nexus, Artifactory
  - `*.s3.amazonaws.com`, `storage.googleapis.com`, `*.blob.core.windows.net`
- **Configuration endpoints:**
  - `/config`, `/api/v1/config`, `/env`, `/.env`
  - `/api/v1/settings` (с лишними полями)
- **Source maps:** `*.js.map`, `*.css.map`
- **Git:** `/.git/config`, `/.git/HEAD`, `/.git/logs/`
- **Swagger / OpenAPI:** `/swagger.json`, `/openapi.json`, `/api-docs`
- **GraphQL introspection:** скрытые поля с секретами
- **Error messages:** stack trace с путями, версиями, секретами
- **HTML-комментарии:** `<!-- TODO: remove key -->`

## Типы секретов
- API keys, JWT-секреты
- DB credentials (connection string)
- Cloud credentials (AWS/GCP/Azure)
- TLS private keys
- Session secrets
- Internal tokens (service-to-service)
- SMTP / webhook credentials

## Инструменты
- `trufflehog`, `gitleaks` (по репозиториям)
- `nuclei` (exposed-panels, exposures)
- `ffuf` по словарю debug/config
- `S3Scanner`, `GCPBucketBrute`
- `curl` + `jq` (ручной анализ)

## Чек-лист
- [ ] Прогнать словарь debug/config/actuator endpoints
- [ ] Проверить `/metrics`, `/health`, `/status` на лишние поля
- [ ] Проверить телеметрию / analytics / events
- [ ] Проверить публичные buckets / registries / artifact storage
- [ ] Проверить source maps
- [ ] Проверить `/.git/`, `/.env`, `/swagger.json`, `/openapi.json`
- [ ] Проверить GraphQL introspection
- [ ] Проверить error messages / stack traces
- [ ] Проверить HTML-комментарии
- [ ] **Для каждого секрета — доказать, что он рабочий (без использования за пределами PoC)**

## Не делать
- Не использовать найденные секреты за пределами PoC
- Не выгружать массово buckets / registries
- Не публиковать найденные секреты
- В PoC — маскировать (`AKIA****`, `sk_live_****`)
