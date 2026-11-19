# Policy Management — PT AF Cloud

## Что ищем
Уязвимости в управлении, доставке и применении политик/конфигураций PT Cloud AF.

## Цели (из правил PT)
- Несанкционированно изменить / отключить / откатить / навязать политику защиты **чужому** tenant, domain, agent/border
- Доставить вредоносную конфигурацию или код в клиентский контур
- Нарушить целостность настроек в border / control plane / API конфигурации

## Векторы
- **IDOR в policy API:**
  - `/api/v1/policies/{id}` — чужой ID
  - `/api/v1/agents/{id}/config` — чужой agent
  - `/api/v1/domains/{id}/policy` — чужой domain
- **Mass assignment:** `"tenant_id": "чужой"`, `"enabled": false` в update
- **Откат политики:** нет проверки прав на rollback
- **Навязывание конфигурации:** подмена config в очереди доставки
- **Supply chain:** вредоносный конфиг в artifact storage / registry
- **Через шаблоны правил:** template injection при рендере правил (пересекается с 05-injection/template)
- **Через импорт:** импорт правил из файла (пересекается с 06-file-upload-import)
- **Через GraphQL mutation:** changePolicy, applyConfig

## Инструменты
- Burp Autorize
- Postman / curl
- Diff конфигов до/после
- GraphQL Voyager

## Чек-лист
- [ ] Найти все policy-эндпоинты (CRUD, apply, rollback, export)
- [ ] Проверить IDOR по policy_id / agent_id / domain_id
- [ ] Проверить mass assignment (`tenant_id`, `enabled`, `action`)
- [ ] Проверить rollback без прав
- [ ] Проверить доставку конфигурации (что видит agent/border)
- [ ] Проверить artifact storage / registry на подмену
- [ ] Проверить GraphQL mutations
- [ ] Проверить импорт правил (см. 06-file-upload-import)

## Не делать
- Не менять реальные политики клиентов
- PoC — только в тестовом tenant
- Не вызывать массовый рестарт agents/borders (DoS)
