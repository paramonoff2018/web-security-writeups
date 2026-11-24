#!/usr/bin/env python3
"""filter_noise.py - очистка сырых логов сканеров перед подачей в LLM.

Удаляет: дубли, статику (.js/.css/.png/.woff/.ico), типовые 404/403,
группирует по (status_code, content_length) и выводит компактную сводку.

Usage:
  python3 filter_noise.py <input_file> [--out filtered/summary.txt]
"""
import sys
import os
import re
from collections import defaultdict

STATIC_EXT = re.compile(r"\.(js|css|png|jpe?g|gif|svg|woff2?|ttf|eot|ico|map)(\?|$)", re.I)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    inp = sys.argv[1]
    out = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]

    with open(inp, errors="ignore") as f:
        lines = [l.rstrip() for l in f if l.strip()]

    # 1. удаляем дубли, сохраняя порядок
    seen = set()
    uniq = []
    for l in lines:
        if l not in seen:
            seen.add(l)
            uniq.append(l)

    # 2. классифицируем
    static, interesting, noise = [], [], []
    for l in uniq:
        if STATIC_EXT.search(l):
            static.append(l)
        elif re.search(r"(404|403|400|401|405)\b", l):
            noise.append(l)
        else:
            interesting.append(l)

    # 3. группировка по коду и длине (для строк вида "status length url")
    groups = defaultdict(list)
    for l in interesting:
        m = re.match(r"^\s*(\d{3})\s+(\d+)\s+(.+)$", l)
        if m:
            groups[(m.group(1), m.group(2))].append(m.group(3))
        else:
            groups[("raw", "")].append(l)

    result = []
    result.append("INPUT: {} (total={}, unique={})".format(inp, len(lines), len(uniq)))
    result.append("STATIC: {} | NOISE(4xx): {} | INTERESTING: {}".format(len(static), len(noise), len(interesting)))
    result.append("")
    result.append("=== INTERESTING (grouped by status+length) ===")
    for (code, ln), urls in sorted(groups.items(), key=lambda x: -len(x[1])):
        result.append("\n[{} | len={} | count={}]".format(code, ln, len(urls)))
        for u in urls[:15]:
            result.append("  {}".format(u))
        if len(urls) > 15:
            result.append("  ... +{} more".format(len(urls) - 15))

    text = "\n".join(result)
    if out:
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        with open(out, "w") as f:
            f.write(text)
        print("[+] saved to {}".format(out))
    else:
        print(text)


if __name__ == "__main__":
    main()
