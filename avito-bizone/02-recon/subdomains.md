# Subdomains

## Пассивная разведка

### Основные домены в скоупе
- [ ] www.avito.ru
- [ ] api.avito.ru
- [ ] m.avito.ru
- [ ] payments.avito.ru
- [ ] *.hrbt.ru
- [ ] *.hmsg.me
- [ ] hrmka.ru
- [ ] *.haraba.ru
- [ ] *.maxposter.ru
- [ ] *.hrmessenger.com
- [ ] *.autoteka.ru
- [ ] *.avito.ru (все остальные)

### Источники для поиска поддоменов
- [ ] crt.sh (https://crt.sh/?q=%25.avito.ru)
- [ ] crt.sh (https://crt.sh/?q=%25.hrbt.ru) — и для каждого домена
- [ ] SecurityTrails
- [ ] Shodan
- [ ] AlienVault OTX
- [ ] Wayback Machine (https://web.archive.org/cdx/search/cdx?url=*.avito.ru&output=txt&fl=original)
- [ ] Google dork: `site:*.avito.ru -www`

### Инструменты (локально в Kali/WSL)
```bash
subfinder -d avito.ru -o subdomains-avito.txt
subfinder -d hrbt.ru -o subdomains-hrbt.txt
# ... для каждого корневого домена
```

> Результаты сохранить ниже