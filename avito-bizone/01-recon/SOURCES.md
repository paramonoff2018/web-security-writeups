# OSINT Sources — Avito

## Поддомены
- **crt.sh** — Certificate Transparency: `https://crt.sh/?q=%25.avito.ru`
- **subfinder** (пассивные источники): Shodan, Censys, VirusTotal, SecurityTrails, AlienVault, urlscan
- **Готовый снимок (2026-08-10):** 157 поддоменов, включая `adm.avito.ru`, `bi-test.avito.ru`, `business.avito.ru`, `api-ast-to-hd.avito.ru`

## Historical URLs / Endpoints
- **Wayback Machine** — `web.archive.org`
- **Common Crawl** — `index.commoncrawl.org`
- **urlscan.io** — снимки и запросы
- **gau** — объединяет несколько источников

## GitHub / GitLab
- Поиск: `"avito.ru" site:github.com`
- `github-subdomains` — извлекает поддомены из публичного кода
- **Не репортить** «секрет без влияния»

## API
- **OpenAPI Авито:** `https://www.avito.ru/developers/api-catalog`
- Снапшот: 248 путей / 256 операций
- Business API: `https://api.avito.ru`, OAuth2 (Client Credentials / Authorization Code)

## Публичные публикации / writeups
- Искать CVE по стеку (после фингерпринтинга)
- Искать writeups по Avito (HackerOne, Habr, Medium)
- **Не использовать** нелегальные сливы ПДн как источник таргетов — только для понимания экосистемы
