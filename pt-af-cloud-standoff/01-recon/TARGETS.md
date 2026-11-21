# Prioritized Targets — PT AF Cloud

## Приоритет 1 (WAF Bypass)
| Хост / цель | Что смотреть | Папка |
|---|---|---|
| `test-ui-megahiddensuffix.ptcloud.ru` | тестовое приложение для обходов | `10-af-bypass/` |
| `af.ptcloud.ru` | парсерные дифференциалы, chunked, HTTP/2 | `10-af-bypass/` |
| `demo.ptcloud.ru` | безопасная среда для проверки гипотез | `10-af-bypass/` |

## Приоритет 2 (Control Plane / API)
| Хост / цель | Что смотреть | Папка |
|---|---|---|
| `auth.ptcloud.ru` | обход аутентификации, session/token | `02-auth-session/` |
| `af.ptcloud.ru` (консоль) | Stored XSS, injection, SSRF, утечка секретов | `03-api-console/` (создать при необходимости) или `05-injection/`, `07-xss/`, `08-ssrf/` |
| `grafana.infra.ptcloud.ru` | debug endpoints, утечка телеметрии | `13-secrets-leaks/` |

## Приоритет 3 (Изоляция тенантов)
| Цель | Вектор | Папка |
|---|---|---|
| Объекты с `tenant_id`, `customer_id`, `folder_id`, `domain_id` | доступ к чужому тенанту | `03-tenant-isolation/` |
| Политики защиты | изменение/отключение чужой политики | `04-policy-management/` |
| Отчёты / инциденты | чтение чужих отчётов | `03-tenant-isolation/` |

## Приоритет 4 (Агенты / Border)
| Цель | Вектор | Папка |
|---|---|---|
| Агенты (WinServer-lab) | RCE, sandbox escape, чтение секретов | `11-agent-vulns/`, `12-rce-sandbox/` |
| Border-компоненты | утечка трафика, заголовков, cookies, конфигов | `11-agent-vulns/`, `13-secrets-leaks/` |
| Механизмы применения политик | DoS/рестарт (только безопасный PoC) | `14-dos-safe-poc/` |

## Особое внимание (в правилах выделено)
- **Stored XSS** в интерфейсе управления → `07-xss/`
- **SQL/NoSQL/LDAP/template/command injection** → `05-injection/`
- **SSRF** в консоли, API, control plane → `08-ssrf/`
- **Log injection / log forging** → `09-log-injection/`
- **Утечка секретов** через телеметрию, debug endpoints → `13-secrets-leaks/`
