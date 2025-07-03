import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes

# === Environment Variables ===
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# === Flask App ===
app = Flask(__name__)

# === Create Telegram Application ===
application: Application = ApplicationBuilder().token(TOKEN).build()


# === Telegram Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))


# === Webhook Route ===
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)

    async def process():
        await application.process_update(update)

    asyncio.run(process())
    return "OK", 200


# === Main Runner ===
if __name__ == "__main__":
    async def run():
        await application.initialize()
        await application.bot.set_webhook(url=WEBHOOK_URL)
        print("Webhook set to:", WEBHOOK_URL)

    asyncio.run(run())
    app.run(host="0.0.0.0", port=10000)
