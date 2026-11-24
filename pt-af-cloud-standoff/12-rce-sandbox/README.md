# RCE / Sandbox Escape — PT AF Cloud

## Что ищем
Уязвимости, приводящие к выполнению произвольного кода, выходу из sandbox/container, чтению секретов, нарушению целостности настроек в border / control plane / API конфигурации.

## Категории (из правил PT)
- Выполнение произвольного кода (RCE)
- Выход из sandbox / container
- Чтение секретов
- Нарушение целостности настроек в border / control plane / API
- Небезопасная десериализация
- Другие способы выполнения кода — **только с безопасным PoC**

## Векторы
- **Десериализация:**
  - Java: ysoserial, gadget chains (CommonsCollections, Spring, Jackson)
  - PHP: phpggc
  - Python: pickle, PyYAML (`!!python/object`)
  - .NET: ysoserial.net
  - Node.js: node-serialize, `eval` в конфигах
- **SSTI → RCE:** см. `05-injection/template`
- **Command injection → RCE:** см. `05-injection/command`
- **File upload → RCE:** см. `06-file-upload-import`
- **Sandbox escape:**
  - `/proc/self/root`, `mount`, `nsenter`, `ptrace`
  - Docker socket (`/var/run/docker.sock`)
  - `CAP_SYS_ADMIN`, `CAP_DAC_READ_SEARCH`
  - cgroup release_agent
- **Secret reading:**
  - `/proc/1/environ`, `/run/secrets/`, env vars
  - Kubernetes service account token (`/var/run/secrets/kubernetes.io/serviceaccount/token`)
- **Supply chain:**
  - Вредоносный конфиг в artifact storage / registry
  - Подмена бинаря при обновлении

## ⚠️ Ограничения PT (критично!)
- **PoC — только безопасный:** `id`, `whoami`, `hostname`, чтение `/etc/hostname`
- **Никаких reverse shell с persistence**
- **Никаких cryptominer'ов**
- **Никаких destructive payload'ов**
- **Никакого выхода за пределы тестового тенанта**
- **Не читать реальные секреты клиентов** (только тестовые)
- **Не выполнять код в реальном клиентском контуре**

## Как валидировать
1. **RCE подтверждён:** команда `id` вернула вывод в ответе / OOB.
2. **Только в тестовом тенанте:** явно указать в отчёте.
3. **Безопасно:** нет persistence, нет reverse shell, нет destructive.
4. **Скриншот / лог:** вывод `id` + контекст (URL, payload).

## Инструменты
- ysoserial, ysoserial.net, phpggc
- tplmap
- JNDI-Exploit-Kit
- interactsh
- `docker` / `nsenter` (для sandbox-escape)

## Чек-лист
- [ ] Найти точки десериализации (cookies, API, импорт, очередь)
- [ ] Проверить Java / PHP / Python / .NET / Node gadgets
- [ ] Проверить SSTI → RCE
- [ ] Проверить command injection → RCE
- [ ] Проверить file upload → RCE
- [ ] Проверить sandbox-escape (docker.sock, capabilities, cgroup)
- [ ] Проверить чтение секретов (`/proc/1/environ`, K8s SA token)
- [ ] Проверить supply chain (artifact storage, registry)
- [ ] **Для каждого — безопасный PoC только в тестовом тенанте**

## Не делать
- Не оставлять webshell / persistence
- Не выполнять `rm -rf`, `dd`, шифрование
- Не pivot в реальную инфраструктуру
- Не читать реальные секреты клиентов
