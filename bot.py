import websocket
import json
import threading
import time

BOT_TOKEN = "REMPLACE_PAR_TON_TOKEN"

IDENTIFY = {
    "op": 2,
    "d": {
        "token": BOT_TOKEN,
        "intents": 0,
        "properties": {
            "os": "linux",
            "browser": "SydneyRP",
            "device": "SydneyRP"
        },
        "presence": {
            "status": "online",
            "activities": [{"name": "🎮 Sydney RP", "type": 0}],
            "since": None,
            "afk": False
        }
    }
}

heartbeat_interval = None
sequence = None

def send_heartbeat(ws):
    global sequence
    while True:
        if heartbeat_interval:
            time.sleep(heartbeat_interval / 1000)
            try:
                ws.send(json.dumps({"op": 1, "d": sequence}))
                print(f"💓 Heartbeat (seq: {sequence})")
            except:
                break

def on_message(ws, message):
    global heartbeat_interval, sequence
    data = json.loads(message)
    op = data.get("op")
    if data.get("s"):
        sequence = data["s"]
    if op == 10:
        heartbeat_interval = data["d"]["heartbeat_interval"]
        threading.Thread(target=send_heartbeat, args=(ws,), daemon=True).start()
        ws.send(json.dumps(IDENTIFY))
    elif op == 0 and data.get("t") == "READY":
        print(f"🟢 Bot EN LIGNE : {data['d']['user']['username']}")
    elif op == 9:
        time.sleep(5)
        connect()

def on_close(ws, *args):
    print("🔴 Déconnecté — Reconnexion...")
    time.sleep(5)
    connect()

def on_error(ws, error):
    print(f"❌ Erreur: {error}")

def connect():
    ws = websocket.WebSocketApp(
        "wss://gateway.discord.gg/?v=10&encoding=json",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

print("🚀 Démarrage Gateway Sydney RP...")
connect()
