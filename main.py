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

# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! ✅ AshisF&Obot is active 💹")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 *Status:* Bot is running perfectly.\n— by Ràñi 💞", parse_mode="Markdown")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_sample_signal()
    await update.message.reply_text(message, parse_mode="Markdown")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("status", status))
application.add_handler(CommandHandler("signal", signal))

# --- Webhook Routes ---
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "OK"

@app.route("/", methods=["GET"])
async def index():
    await application.bot.set_webhook(WEBHOOK_URL)
    return "✅ Webhook set for AshisF&Obot"

# --- Start the bot ---
if __name__ == "__main__":
    import asyncio
    async def run():
        await application.initialize()
        await application.start()
        await application.bot.set_webhook(WEBHOOK_URL)
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    asyncio.run(run())
