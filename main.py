import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
WEBHOOK_URL = f"https://ashisfnobot.onrender.com/{TOKEN}"  # Your live URL

app = Flask(__name__)

# Initialize the bot
application = Application.builder().token(TOKEN).build()

# Define command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is working 💹")

application.add_handler(CommandHandler("start", start))

# Flask route to receive webhook POST requests
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.create_task(application.update_queue.put(update))
    return "OK"

# Root URL - sets webhook
@app.route("/", methods=["GET"])
async def set_webhook():
    success = await application.bot.set_webhook(url=WEBHOOK_URL)
    return f"Webhook set: {success}"

# Start Flask and bot
if __name__ == "__main__":
    async def main():
        await application.initialize()
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

    asyncio.run(main())
