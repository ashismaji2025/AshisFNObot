import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Environment Variables
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Initialize Flask
app = Flask(__name__)

# Initialize Telegram Bot
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# Webhook Route
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        asyncio.run(application.process_update(update))
        return "OK", 200

# Set Webhook Once at Startup
@app.before_first_request
def setup_webhook():
    asyncio.run(bot.set_webhook(url=WEBHOOK_URL))
    print("Webhook set to:", WEBHOOK_URL)

# Run Flask
if __name__ == "__main__":
    app.run(port=10000, host="0.0.0.0")
