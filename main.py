import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Environment Variables ===
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# === Flask App ===
app = Flask(__name__)

# === Event Loop and Telegram Bot App ===
loop = asyncio.get_event_loop()
application = ApplicationBuilder().token(TOKEN).build()
bot = application.bot

# === Telegram Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# Optional: Basic homepage route to prevent 404
@app.route("/", methods=["GET"])
def home():
    return "AshisF&Obot is alive and running 💕", 200
# === Webhook Route ===
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        asyncio.run_coroutine_threadsafe(application.process_update(update), loop)
        return "OK", 200
    except Exception as e:
        print("❌ Error in /webhook:", e)
        return "Webhook Error", 500

# === Startup Initializer ===
async def startup():
    await application.initialize()
    await application.start()
    await bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook set to:", WEBHOOK_URL)

# === Run Everything ===
if __name__ == "__main__":
    loop.run_until_complete(startup())
    app.run(host="0.0.0.0", port=10000)
