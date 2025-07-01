import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_URL = "https://ashisfnobot.onrender.com/webhook"

app = Flask(__name__)

# --- Telegram bot setup ---
application = ApplicationBuilder().token(TOKEN).build()

# --- Telegram command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis 💕! Your bot is live with webhook.")

application.add_handler(CommandHandler("start", start))

# --- Flask webhook route ---
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.get_event_loop().create_task(application.process_update(update))
    return "ok", 200

# --- Set webhook only once ---
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook set successfully.")

# --- Main block ---
if __name__ == "__main__":
    # Set webhook (only once on startup)
    asyncio.get_event_loop().run_until_complete(set_webhook())

    # Bind Flask to Render-assigned port
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
