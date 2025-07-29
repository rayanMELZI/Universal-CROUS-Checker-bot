from flask import Flask
import threading
from checkers import start_checker_loop, start_ping_loop
from bot import handle_webhook
import os

app = Flask(__name__)
app.route("/")(lambda: "✅ Bot CROUS Universel actif.")
app.route("/webhook", methods=["POST"])(handle_webhook)

if __name__ == "__main__":
    threading.Thread(target=start_checker_loop, daemon=True).start()
    threading.Thread(target=start_ping_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
