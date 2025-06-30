import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_URL = f"https://ashisfnobot.onrender.com/{TOKEN}"

# Initialize Flask app
app = Flask(__name__)

# Create Telegram app (without ApplicationBuilder)
application = Application.builder().token(TOKEN).build()

# Async command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is working 💹")

application.add_handler(CommandHandler("start", start))

# Webhook route for Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

# Just a health check
@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is running."

# Start everything
if __name__ == "__main__":
    async def run():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL)
        await application.start()
    asyncio.run(run())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
