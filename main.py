import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Environment ===
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# === Flask App ===
app = Flask(__name__)

# === Telegram Bot & Application ===
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# === Telegram Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your bot is working 💕")

application.add_handler(CommandHandler("start", start))

# === Webhook Route ===
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    async def process_update():
        await application.initialize()
        await application.process_update(update)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_update())
    return "OK", 200


# === Main App Runner ===
if __name__ == "__main__":
    # Set webhook before running Flask app
    asyncio.run(bot.set_webhook(url=WEBHOOK_URL))
    print("Webhook set to:", WEBHOOK_URL)

    app.run(host="0.0.0.0", port=10000)
