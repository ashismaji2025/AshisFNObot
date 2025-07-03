import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Initialize Flask app
app = Flask(__name__)

# Telegram Bot and Application
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# --- Webhook Endpoint ---
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)

        # Run async methods synchronously inside Flask thread
        async def handle_update():
            await application.initialize()
            await application.process_update(update)

        asyncio.run(handle_update())
        return "OK", 200

# --- Root Route for Health Check ---
@app.route("/", methods=["GET"])
def index():
    return "AshisFNObot is live 🚀", 200

# --- Set Webhook at Startup ---
@app.before_first_request
def set_webhook():
    asyncio.run(bot.set_webhook(url=WEBHOOK_URL))
    print(f"✅ Webhook set to: {WEBHOOK_URL}")

# --- Run Flask App ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
