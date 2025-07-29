import os, json, requests
from flask import request
from utils import add_log, send_message, send_keyboard, save_user

def handle_webhook():
    data = request.json
    print("✅ Webhook reçu", flush=True)
    print(json.dumps(data, indent=2), flush=True)

    try:
        if "message" in data:
            message = data["message"]
            text = message.get("text", "")
            chat_id = str(message["chat"]["id"])
            print(f"📩 Message: {text} — de {chat_id}", flush=True)

            if text == "/start":
                send_keyboard(chat_id)
            elif text.lower() == "/lyon":
                save_user(chat_id, "Lyon")
                send_message(chat_id, "✅ Tu recevras les alertes CROUS pour Lyon.")
            elif text.lower() == "/paris":
                save_user(chat_id, "Paris")
                send_message(chat_id, "✅ Tu recevras les alertes CROUS pour Paris.")
            else:
                send_message(chat_id, "❓ Choisis une ville depuis le menu.")
        return "ok"
    except Exception as e:
        print(f"❌ Erreur dans handle_webhook: {e}", flush=True)
        return "error"