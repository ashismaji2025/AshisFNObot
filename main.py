import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_URL = "https://ashisfnobot.onrender.com/webhook"

app = Flask(__name__)

application = ApplicationBuilder().token(TOKEN).build()

# --- Telegram command ---
async def start(update: Update, context):
    await update.message.reply_text("Hello Ashis 💕! Your bot is live with webhook.")

application.add_handler(CommandHandler("start", start))

# --- Webhook route ---
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.run(application.process_update(update))  # ✅ CORRECT
        return "ok"

# --- Main block ---
if __name__ == "__main__":
    async def run():
        await application.initialize()
        await application.start()
        await application.bot.set_webhook(WEBHOOK_URL)
        print("✅ Bot initialized and webhook set!")

    asyncio.run(run())

    # 🧠 Render needs this!
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
