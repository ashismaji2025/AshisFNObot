import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

# Get token and webhook URL from environment
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Setup Flask app and Telegram Bot
app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, update_queue=None, workers=0, use_context=True)

# Command handler
def start(update, context):
    update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

dispatcher.add_handler(CommandHandler("start", start))

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Set webhook when Flask starts
@app.before_first_request
def setup_webhook():
    bot.set_webhook(WEBHOOK_URL)
    print("Webhook set to:", WEBHOOK_URL)

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
