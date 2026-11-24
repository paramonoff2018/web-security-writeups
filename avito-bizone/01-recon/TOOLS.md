# Tools Inventory — Avito

## OSINT / Поддомены
| Инструмент | Назначение | Команда |
|---|---|---|
| subfinder | пассивный enum | `subfinder -d avito.ru -all -recursive -o subs.txt` |
| assetfinder | быстрый enum | `assetfinder --subs-only avito.ru` |
| amass | комплексный enum | `amass enum -passive -d avito.ru` |
| findomain | быстрый enum | `findomain -t avito.ru -u` |
| crt.sh | Certificate Transparency | `curl -s "https://crt.sh/?q=%25.avito.ru&output=json"` |

## JS / Historical URLs
| Инструмент | Назначение | Команда |
|---|---|---|
| waybackurls | URL из Wayback | `waybackurls avito.ru` |
| gau | объединяет источники | `gau avito.ru` |
| katana | краулинг + JS-парсинг | `katana -u https://www.avito.ru -d 3 -jc` |
| LinkFinder | эндпоинты из JS | `python3 linkfinder.py -i <url> -d` |
| jsluice | парсинг JS | `jsluice urls <js_file>` |
| SecretFinder | поиск секретов в JS | `python3 SecretFinder.py -i <url>` |

## Активная разведка
| Инструмент | Назначение | Команда |
|---|---|---|
| httpx | живость + tech detect | `httpx -l subs.txt -title -tech-detect -status-code` |
| whatweb | фингерпринтинг | `whatweb -i hosts.txt` |
| puredns | массовый резолвинг | `puredns resolve subs.txt` |
| naabu | сканер портов | `naabu -list hosts.txt -top-ports 1000` |

## Скриншоты
| Инструмент | Назначение |
|---|---|
| Aquatone | скриншоты всех хостов |
| EyeWitness | скриншоты + отчёт |

## Поиск уязвимостей
| Инструмент | Назначение | Заметки |
|---|---|---|
| Burp Community | ручное тестирование | Proxy, Repeater, Intruder (throttle) |
| nuclei | автошаблоны | `-severity medium,high,critical`, осторожно |
| ffuf | fuzzing | маленькие словари |

## Мобильное (только при обосновании)
| Инструмент | Назначение |
|---|---|
| apktool | статика APK |
| mitmproxy | перехват трафика |
| Frida | динамический анализ (root/jailbreak) |
