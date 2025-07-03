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

# === Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# === Webhook Route ===
@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
        return "OK", 200

# === Auto Webhook Setup and App Run ===
if __name__ == "__main__":
    async def main():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)
        print("Webhook set to:", WEBHOOK_URL)
        app.run(host="0.0.0.0", port=10000)

    asyncio.run(main())
