from flask import Flask, request
from bot import app_bot, setup_handlers
import os

app = Flask(__name__)

setup_handlers(app_bot)

@app.route("/")
def index():
    return "✅ Le bot CROUS est en ligne."

@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        await app_bot.update_queue.put(request.json)
        return "ok"

if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()
    PORT = int(os.getenv("PORT", 5000))

    # Lancer l'application Flask et le bot Telegram
    loop = asyncio.get_event_loop()
    app_bot.initialize()
    app.run(host="0.0.0.0", port=PORT)
