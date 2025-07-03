import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram application
application = ApplicationBuilder().token(TOKEN).build()

# Define bot command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

# Add command handler
application.add_handler(CommandHandler("start", start))

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)

    async def handle():
        await application.initialize()
        await application.process_update(update)

    asyncio.run(handle())
    return "OK", 200

# Health check route
@app.route("/", methods=["GET"])
def index():
    return "✅ AshisFNObot is live", 200

# ✅ Set webhook on startup
async def setup_webhook():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook set to:", WEBHOOK_URL)

# Run setup when script starts
asyncio.run(setup_webhook())

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
