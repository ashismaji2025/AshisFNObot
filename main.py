import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

# Environment variables
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Create bot and Flask app
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Dispatcher (sync version, no async)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

# Command handler
def start(update: Update, context):
    update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

dispatcher.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Set webhook once
@app.before_first_request
def set_webhook():
    bot.set_webhook(WEBHOOK_URL)
    print("Webhook set to:", WEBHOOK_URL)

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
