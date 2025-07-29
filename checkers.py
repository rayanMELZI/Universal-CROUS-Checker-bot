import time, os, json
import requests
from utils import add_log, send_email, send_city_telegram

URLS = {
    "Lyon": "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=4.7718134_45.8082628_4.8983774_45.7073666",
    "Paris": "https://trouverunlogement.lescrous.fr/tools/41/search?bounds=1.4462445_49.241431_3.5592208_48.1201456"
}


def check_disponibilite(ville, url):
    try:
        response = requests.get(url)
        if "Aucun logement" in response.text:
            add_log(f"❌ Aucun logement à {ville}")
        else:
            add_log(f"✅ Logement(s) à {ville} !")
            send_email(url, ville)
            send_city_telegram(ville, f"🚨 Logement dispo à {ville} ! Vérifie : {url}")
    except Exception as e:
        add_log(f"⚠️ Erreur vérif {ville} : {e}")


def start_checker_loop():
    while True:
        for ville, url in URLS.items():
            check_disponibilite(ville, url)
        time.sleep(300)  # 5 minutes


def start_ping_loop():
    while True:
        now = time.strftime('%Y-%m-%d %H:%M')
        send_city_telegram("Lyon", f"🟢 Le bot tourne toujours ({now})")
        send_city_telegram("Paris", f"🟢 Le bot tourne toujours ({now})")
        time.sleep(3600)  # 1h

