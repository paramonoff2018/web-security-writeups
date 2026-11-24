# AF Bypass — TLS / HTTPS Inspection

## Что ищем
Обход проверки TLS/HTTPS inspection, если это приводит к:
- неполному анализу трафика
- неверному применению политики

## ⚠️ Главное правило PT
Сам факт «AF не увидел трафик» **не считается обходом**, если backend не исполнил атаку. См. `http-parsing/README.md`.

## Векторы
- **SNI vs Host header:**
  - SNI = `allowed.example.com`, Host = `protected.example.com`
  - AF маршрутизирует по SNI, инспектирует по Host (или наоборот)
- **TLS-версии:**
  - TLS 1.0 / 1.1 (если AF отключает инспекцию для старых версий)
  - TLS 1.3 (если AF не поддерживает)
  - SSLv3 / SSLv2 (вряд ли, но проверить)
- **Шифры:**
  - Экзотические cipher suites (AF не может расшифровать)
  - NULL ciphers
  - EXPORT ciphers
- **Certificate pinning обход:**
  - Если AF делает MITM, а backend пиннит — трафик может идти в обход
- **ALPN:**
  - `h2` vs `http/1.1` — AF может инспектировать только один
- **Client certificate:**
  - mTLS — если AF не поддерживает client cert, трафик идёт напрямую
- **HTTP/3 (QUIC):**
  - Если AF не инспектирует QUIC — трафик идёт в обход
- **Redirect на HTTPS:**
  - HTTP → HTTPS redirect — AF инспектирует только HTTP?
- **HSTS preload:**
  - AF не может инспектировать preloaded HSTS-домены (если так настроено)

## Как валидировать
1. **Backend исполнил:** payload дошёл и сработал (XSS, SQLi, RCE).
2. **AF не инспектировал:** в событиях AF запрос отсутствует или помечен как «не инспектирован».
3. **Политика не применилась:** AF должен был заблокировать, но не заблокировал.

## Инструменты
- `openssl s_client` (SNI, версии, шифры)
- `curl --tls-max 1.2` / `--tlsv1.3`
- `nmap --script ssl-enum-ciphers`
- `testssl.sh`
- `h2load`, `nghttp` (HTTP/2)
- `quiche`, `curl --http3` (HTTP/3)

## Чек-лист
- [ ] SNI vs Host header mismatch
- [ ] TLS 1.0 / 1.1 / 1.3
- [ ] Экзотические шифры
- [ ] ALPN (`h2` vs `http/1.1`)
- [ ] Client certificate (mTLS)
- [ ] HTTP/3 (QUIC)
- [ ] HTTP → HTTPS redirect
- [ ] **Для каждого — доказать, что backend исполнил, а AF не инспектировал**
- [ ] Проверить, что политика AF не применилась

## Не делать
- Не считать «AF не увидел» = «обход» без PoC на backend
- Не использовать SSL-недостатки без эксплуатации (out-of-scope)
- Не тестировать на реальных клиентах
