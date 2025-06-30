import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from signals import get_sample_signal

# Get token from environment
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"

# Initialize Flask and Bot App
app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is working 💹")

# Command: /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signal = get_sample_signal()
    await update.message.reply_markdown(signal)

# Register commands
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))

# Telegram webhook endpoint
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Root check
@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is running."

# Startup code
if __name__ == "__main__":
    import asyncio
    async def start_bot():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)
        print("✅ Webhook set.")

    asyncio.run(start_bot())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
