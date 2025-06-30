import os
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
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
async def index():
    # Optional: Set webhook if not already set
    await application.bot.set_webhook(WEBHOOK_URL)
    return "AshisFNObot is running with webhook ✅"

if __name__ == "__main__":
    import asyncio
    async def run():
        await application.initialize()
        await application.start()
        await application.updater.start_polling()  # Not used, safe to remove
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    asyncio.run(run())
