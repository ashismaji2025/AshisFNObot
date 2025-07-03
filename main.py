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

# === Initialize Telegram Application ===
application = ApplicationBuilder().token(TOKEN).build()
bot = application.bot

# === Telegram Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# === Webhook Route ===
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.create_task(application.process_update(update))
    return "OK", 200

# === One-time async initialization (including webhook) ===
async def init():
    await application.initialize()
    await bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook set to:", WEBHOOK_URL)

# === Run Everything ===
if __name__ == "__main__":
    asyncio.run(init())  # Set webhook + init
    app.run(host="0.0.0.0", port=10000)
