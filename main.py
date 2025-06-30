import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from signals import get_sample_signal

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is working 💹")

# /status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signal = get_sample_signal()
    await update.message.reply_markdown(signal)

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is live 🌐"

if __name__ == "__main__":
    import threading
    import asyncio

    async def setup():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)
        await application.start()
        print("Webhook set and application started.")

    threading.Thread(target=lambda: asyncio.run(setup())).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
