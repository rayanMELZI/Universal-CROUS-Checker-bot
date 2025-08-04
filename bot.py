from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

app_bot = Application.builder().token(TOKEN).build()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bonjour ! Je suis un bot qui peut surveiller les logements CROUS dans plusieurs villes. Tape /help pour plus d'infos.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Je surveille les logements CROUS pour vous. Choisissez une ville et je vous enverrai une alerte dès qu'un logement est dispo !")


def handle_response(text: str) -> str:
    processed = text.lower()

    if "bonjour" in processed or "salut" in processed:
        return "👋 Salut !"
    if "merci" in processed:
        return "Avec plaisir ! 😊"
    return "Désolé, je n'ai pas compris. Essayez une commande comme /start ou /help."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat.id
    print(f"📩 Message reçu de {chat_id}: {text}", flush=True)

    response = handle_response(text)
    await update.message.reply_text(response)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"⚠️ Erreur : {context.error}", flush=True)


# Ajoute tous les handlers
def setup_handlers(app):
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error_handler)
