# Prioritized Targets — Avito

## Приоритет 1 (первая неделя)
| Хост | Что смотреть | Папка |
|---|---|---|
| `adm.avito.ru` | админка, слабая авторизация, вертикальная эскалация | `02-auth-session`, `03-access-control`, `11-privilege-escalation` |
| `bi-test.avito.ru` | тестовый стенд — часто менее защищён | `03-access-control`, `04-idor` |
| `api.avito.ru` | эндпоинты с user_id/item_id/chat_id — IDOR | `04-idor`, `05-injection` |
| `business.avito.ru` | логика лимитов, промо | `09-limit-bypass` |
| AI-сервисы (hrmessenger, hrmost, autoteka, haraba) | prompt injection, excessive agency, утечка данных | `10-info-disclosure` |

## Приоритет 2 (по результатам)
| Хост | Что смотреть |
|---|---|
| `m.avito.ru` | мобильная версия — XSS, open redirect, логика |
| `www.avito.ru` | основной интерфейс — XSS, бизнес-логика |
| `*.avito.ru` (dev/staging) | утечки конфигов, отладочные эндпоинты |

## Особое внимание (в правилах Avito выделено отдельно)
- **Утечка телефонов:** возможность запросить телефон без отдельных эндпоинтов; узнать из объявлений в статусах "закрыт"/"на модерации" → `10-info-disclosure`
- **VIN-номера:** полные VIN вместе с ПДн → `10-info-disclosure`
- **Обход лимитов** бесплатных операций → `09-limit-bypass`
- **Open redirect без промежуточной страницы** → `08-open-redirect`

## Race Conditions — отдельный приоритет
| Цель | Вектор | Папка |
|---|---|---|
| `api.avito.ru` (OAuth) | race condition в token store → утечка токенов | `02-auth-session` |
| `business.avito.ru` | лимиты публикаций/промо → обход | `09-limit-bypass` |
| Купоны/промокоды | limit overrun | `09-limit-bypass` |
| Рейтинги/лайки | многократное голосование | `03-access-control` |
