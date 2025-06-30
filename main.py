import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_URL = f"https://ashisfnobot.onrender.com/{TOKEN}"

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# Command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is working 💹")

application.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is running."

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

async def main():
    # Start Flask in separate thread
    threading.Thread(target=run_flask).start()

    await application.initialize()
    await application.bot.set_webhook(url=WEBHOOK_URL)
    await application.start()
    await application.updater.start_polling()  # Optional, won't run since webhook handles updates
    await application.updater.wait_until_closed()  # Wait forever

if __name__ == "__main__":
    asyncio.run(main())
