# Tools — PT AF Cloud

## Разведка
| Инструмент | Назначение |
|---|---|
| subfinder / assetfinder / amass | пассивный enum поддоменов |
| crt.sh | Certificate Transparency |
| httpx | живость + tech detect |
| whatweb / Wappalyzer | фингерпринтинг |
| Aquatone / EyeWitness | скриншоты |
| naabu | порты (точечно) |

## WAF Bypass
| Инструмент | Назначение |
|---|---|
| **Burp Suite Community** | Repeater, Intruder, Turbo Intruder (BApp) |
| **Turbo Intruder** | last-byte sync, race conditions, single-packet attack |
| **racey** (Go) | HTTP/2/3 параллельные запросы |
| **Hackvertor** (Burp BApp) | кодировки: hex, XML, Unicode, base64 |
| **curl --parallel** | простой параллельный запуск |

## Injection / API
| Инструмент | Назначение |
|---|---|
| sqlmap | SQLi (осторожно, throttle) |
| nuclei | шаблоны (осторожно) |
| ffuf | fuzzing эндпоинтов |
| Postman / Insomnia | ручное тестирование API |

## Специфика PT AF
| Инструмент | Назначение |
|---|---|
| **WinServer-lab** (VB) | тестирование агентов и border-компонентов |
| mitmproxy | перехват трафика агентов |
| Wireshark | анализ HTTP/2, chunked, WebSocket |
