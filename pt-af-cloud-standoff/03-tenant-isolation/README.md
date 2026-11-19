# Tenant Isolation — PT AF Cloud

## Что ищем
Нарушение изоляции tenant / customer / folder / domain. Это одна из ключевых целей программы PT.

## Уровни изоляции
- **Tenant** — верхний уровень (клиент PT Cloud AF)
- **Customer** — под-уровень (бизнес-единица)
- **Folder** — группировка ресурсов
- **Domain** — защищаемый домен
- **User / Role** — пользователи внутри tenant

## Векторы
- **IDOR по tenant/customer/folder/domain:**
  - Подмена `tenant_id`, `customer_id`, `folder_id`, `domain_id` в API
  - UUID vs числовые ID
- **Чтение чужих отчётов/инцидентов/рекомендаций:**
  - `/api/v1/tenants/{id}/reports`
  - `/api/v1/incidents/{id}`
  - Экспорт в PDF/CSV
- **Запись/изменение чужого:**
  - Создание правила в чужом tenant
  - Изменение политики чужого домена
- **Кросс-tenant через shared-ресурсы:**
  - Общие бакеты / registries / artifact storage
  - Публичные buckets
- **Через API vs UI:**
  - UI скрывает чужой tenant, API — нет
- **Через GraphQL:**
  - Aliases / fragments на чужие ID
  - Introspection скрытых полей

## Инструменты
- Burp Autorize (2 тенанта / 2 роли)
- Postman
- ffuf по UUID (но не массово!)
- GraphQL Voyager / InQL

## Чек-лист
- [ ] Создать 2 тенанта (или 2 customer/folder) в тестовом окружении
- [ ] Собрать запросы tenant A, повторить с токеном tenant B → 403/404?
- [ ] Проверить все ID в query/body/headers/GraphQL
- [ ] Проверить экспорт отчётов/инцидентов чужого tenant
- [ ] Проверить shared buckets / registries / artifact storage
- [ ] Проверить GraphQL introspection и aliases
- [ ] Сравнить UI vs API (что скрывает UI)

## Не делать
- Не читать массово чужие данные
- Не менять данные чужого tenant (только PoC на чтение)
- В PoC — 1–2 подтверждения, без массивов
