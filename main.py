import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Environment Variables ===
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# === Initialize Flask App ===
app = Flask(__name__)

# === Initialize Telegram Bot App ===
application = ApplicationBuilder().token(TOKEN).build()
bot = application.bot

# === Telegram Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# === Webhook Route ===
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        asyncio.create_task(application.process_update(update))
        return "OK", 200

# === Startup Tasks: Webhook and Initialization ===
@app.before_first_request
def init_webhook():
    async def setup():
        await application.initialize()
        await bot.set_webhook(WEBHOOK_URL)
        print("Webhook set to:", WEBHOOK_URL)

    asyncio.get_event_loop().create_task(setup())

# === Run Flask ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
