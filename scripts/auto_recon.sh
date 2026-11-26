#!/usr/bin/env bash
# auto_recon.sh - обвязка пассивной разведки Avito с rate limit и прокси.
# Использование: bash auto_recon.sh
# Прокси: Burp (127.0.0.1:8080). Rate limit: 2 RPS максимум.

set -u
cd "$(dirname "$0")/.." || exit 1

ROOT_DOMAINS="avito.ru hrbt.ru hmsg.me hrmka.ru haraba.ru maxposter.ru hrmessenger.com autoteka.ru"
OUT=raw_logs
FILTERED=filtered
mkdir -p "$OUT" "$FILTERED"
export PATH="$PATH:$HOME/go/bin"

echo "[+] Pass 1: subfinder (passive)"
for d in $ROOT_DOMAINS; do
  echo "    - $d"
  subfinder -d "$d" -all -silent -timeout 15 >> "$OUT/subs_raw.txt" 2>/dev/null
  sleep 1
done

echo "[+] Dedup"
sort -u "$OUT/subs_raw.txt" > "$OUT/subs_all.txt"
wc -l "$OUT/subs_all.txt"

echo "[+] Pass 2: httpx (live + tech) через Burp proxy, rate 2/s"
cat "$OUT/subs_all.txt" | httpx -silent -title -tech-detect -status-code \
  -rate-limit 2 -http-proxy http://127.0.0.1:8080 -o "$OUT/subs_live.txt"

echo "[+] Filter noise"
python3 scripts/filter_noise.py "$OUT/subs_live.txt" --out "$FILTERED/subs_summary.txt"

echo "[+] Done. See filtered/subs_summary.txt"
