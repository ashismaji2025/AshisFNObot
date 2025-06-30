import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from signals import get_sample_signal

# Environment
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://ashisfnobot.onrender.com{WEBHOOK_PATH}"
PORT = int(os.environ.get('PORT', 10000))

# Create Flask and Telegram app
app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is active 💹")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot status: Working fine.")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_sample_signal()
    await update.message.reply_text(message, parse_mode="Markdown")

# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("signal", signal))

# Webhook endpoint
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Dummy root (optional)
@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is running 💹"

# Main runner
if __name__ == "__main__":
    import asyncio

    async def run():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)
        print("✅ Webhook set successfully.")
        await application.start()
        await application.updater.start_polling()
        await application.updater.idle()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
