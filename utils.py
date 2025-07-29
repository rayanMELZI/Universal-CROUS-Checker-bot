import os, time, json, smtplib, requests
from dotenv import load_dotenv
load_dotenv()

def add_log(msg):
    print(msg)
    with open("logs.txt", "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} — {msg}\n")

def send_message(chat_id, text):
    token = os.getenv("MAIN_TELEGRAM_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})

def send_keyboard(chat_id):
    token = os.getenv("MAIN_TELEGRAM_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "📍 Quelle ville CROUS veux-tu surveiller ?",
        "reply_markup": {
            "keyboard": [
                [{"text": "/lyon"}],
                [{"text": "/paris"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }
    }
    requests.post(url, json=payload)

def save_user(chat_id, ville):
    users = []
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users = json.load(f)

    for user in users:
        if user["chat_id"] == chat_id:
            user["ville"] = ville
            break
    else:
        users.append({"chat_id": chat_id, "ville": ville})

    with open("users.json", "w") as f:
        json.dump(users, f)

def send_city_telegram(ville, message):
    if not os.path.exists("users.json"):
        return
    with open("users.json", "r") as f:
        users = json.load(f)

    for user in users:
        if user["ville"].lower() == ville.lower():
            send_message(user["chat_id"], message)

def send_email(url, ville):
    email = os.getenv("EMAIL")
    mdp = os.getenv("EMAIL_PASSWORD")
    destinataire = os.getenv("SEND_TO")
    subject = f"Logement CROUS dispo à {ville}"
    body = f"Vérifie ici : {url}"
    msg = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, mdp)
            server.sendmail(email, destinataire, msg)
        add_log(f"📧 Email envoyé pour {ville}")
    except Exception as e:
        add_log(f"❌ Email erreur : {e}")