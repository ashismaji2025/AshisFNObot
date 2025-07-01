import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# ✅ Load token and webhook URL
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_URL = "https://ashisfnobot.onrender.com/webhook"

# ✅ Build and initialize the bot app
application = ApplicationBuilder().token(TOKEN).build()

# ✅ Define Flask app
app = Flask(__name__)

# ✅ Your command handler
async def start(update: Update, context):
    await update.message.reply_text("Hello Ashis 💕! Your bot is now alive!")

application.add_handler(CommandHandler("start", start))

# ✅ Flask webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.run(application.process_update(update))  # 🔧 Fixed async handling
        return "ok", 200

# ✅ Main app runner
if __name__ == "__main__":
    async def run():
        await application.initialize()
        await application.start()
        await application.bot.set_webhook(WEBHOOK_URL)
        print("Bot initialized and webhook set!")

    asyncio.run(run())
    app.run(host="0.0.0.0", port=10000)
