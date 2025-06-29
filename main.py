from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, Dispatcher
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def index():
    return 'AshisFNObot is alive!'

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

def start(update, context):
    update.message.reply_text("Hello Ashis-da! Your AshisFNObot is now active 💹")

from telegram.ext import Updater
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    app.run(port=8080)
