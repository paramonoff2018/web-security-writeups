import asyncio
import websockets
import json

WS_URL = "wss://ws-api.oneme.ru/websocket"
TOKEN = "An_Sx6HQ9HDi-yKdkQ3EzzBSbXmNENSsqORt5fse6X78XhqF5n7GSYaoQr9k0r0EoGB6KIA0n6QLD4DpuH0mjIwEZCXwYxruK6XAOUuUTBxN6r9NKNrXlRXJZQYMtvG8j899XFyQhLu88GEvp3sNGZzMbFtdoE5vZGA4D3Qww4OtcfNJJtv8T6S3Hbso5C5cVKj2aYqp9FjZJBIiM3lvVwafvTKmxNymW5HaEvjsOmobkqu6JYatCS0gSYsfH00sudg_744HtVuG7JnyGazcH512TTQsITmeCaTf5k3opLRGoCkCi-FbV39BqwIHbTqViYUVy4DibbBka5VsdVOn4mPRq6vCyJ6OoMWiuljTklTyczzoB3Y2udNzdFujPiy0EEzEEuxSR9mWHX8iVivbjrqBwosVtveJxiS2sfpQVoWUHCLSs9dKOKf13kGNfAcKve53_VTV0Jsp-20JI8u4WUUlCvn3-x12VFYqg9wus5U4EvfQeWQPBm51quo9Qq_eygA-C9lIwp0x2JXjBVGcdJvdLjHKcuHbsgKnjduI2e2scZMipHMReqEq0StHfHt73v3YEZTCkqQFhap1yIVhH9-FG6Ki-j-jwgrbcnlAZmzEk7UK483rAfPWuWwyQZmByDjDjysf64Kh6Hqdmk91IGIor_XaccqYcXh0qj4NnlRiGQIx0o61QRqF0s_VB1w-7WmbXes"  # Вставь токен Админа
DEVICE_ID = "ab2fd76e-bad0-4d9f-a289-565d465f3ea9"  # Вставь device_id Админа

CHAT_ID = -81072454520980
USER_TO_INVITE = 539596854  # ID Test Max (предполагаемый)

seq_counter = 0

async def send_packet(ws, opcode, payload, cmd=0):
    global seq_counter
    seq_counter += 1
    packet = {
        "ver": 11,
        "cmd": cmd,
        "seq": seq_counter,
        "opcode": opcode,
        "payload": payload
    }
    await ws.send(json.dumps(packet))
    print(f"[->] Отправлен пакет (opcode={opcode}, seq={seq_counter})")
    return seq_counter

async def receive_packet(ws):
    try:
        response = await asyncio.wait_for(ws.recv(), timeout=5.0)
        data = json.loads(response)
        print(f"[<-] Получен ответ (cmd={data.get('cmd')}, seq={data.get('seq')})")
        if data.get("cmd") == 3:
            print(f"[!] ОШИБКА: {data.get('payload')}")
        elif data.get("cmd") == 1:
            print(f"[+] УСПЕХ: {data.get('payload')}")
        return data
    except asyncio.TimeoutError:
        print("[-] Таймаут ожидания ответа.")
        return None
    except websockets.exceptions.ConnectionClosed:
        print("[-] Соединение закрыто.")
        return None

async def main():
    async with websockets.connect(
        WS_URL, 
        origin="https://web.max.ru",
        additional_headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0"}
    ) as ws:
        print("[*] Подключение установлено.")
        
        # 1. INIT
        print("[*] Шаг 1: INIT...")
        await send_packet(ws, 6, {
            "deviceId": DEVICE_ID, 
            "userAgent": {
                "deviceType": "WEB",
                "locale": "ru_RU",
                "osVersion": "Linux",
                "deviceName": "Kali",
                "headerUserAgent": "Mozilla/5.0 (X11; Linux x86_64) Firefox/153.0"
            }
        })
        await receive_packet(ws)
        
        # 2. LOGIN
        print("[*] Шаг 2: LOGIN...")
        await send_packet(ws, 19, {"token": TOKEN})
        resp = await receive_packet(ws)
        
        if not resp or resp.get("cmd") == 3:
            print("[!] Авторизация не удалась. Проверь токен и device_id.")
            return
        print("[+] Авторизация успешна!")

        # 3. Приглашение (Opcode 77 - CHAT_MEMBERS_UPDATE)
        print(f"[*] Шаг 3: Приглашаем {USER_TO_INVITE} в канал {CHAT_ID}...")
        invite_payload = {
            "chatId": CHAT_ID,
            "userIds": [USER_TO_INVITE],
            "operation": "add",
            "showHistory": True
        }
        await send_packet(ws, 77, invite_payload)
        
        # Читаем ответ
        print("[*] Ожидание ответа...")
        for _ in range(3):
            await receive_packet(ws)

if __name__ == "__main__":
    asyncio.run(main())