import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Initialize Flask app
app = Flask(__name__)
bot = Bot(token=TOKEN)

# Create one shared event loop
event_loop = asyncio.get_event_loop()
application = Application.builder().token(TOKEN).loop(event_loop).build()

# Define command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Bot is running 💖")

application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route('/webhook', methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        event_loop.create_task(application.process_update(update))
        return "OK", 200
    except Exception as e:
        print("Webhook Error:", e)
        return "Internal Server Error", 500

# Homepage
@app.route("/")
def home():
    return "🌐 AshisFNObot is live and listening!"

# Set webhook and start Flask
if __name__ == "__main__":
    print("✅ Setting webhook...")
    event_loop.run_until_complete(bot.set_webhook(url=WEBHOOK_URL))
    print("🚀 Bot is running at:", WEBHOOK_URL)
    event_loop.run_until_complete(application.initialize())
    app.run(host="0.0.0.0", port=10000)
