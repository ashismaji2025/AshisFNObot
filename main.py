import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
application = Application.builder().token(BOT_TOKEN).build()

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.get_event_loop_policy().new_event_loop().run_until_complete(application.process_update(update))
        return "ok"
    return "not allowed"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! I am alive 💹📈")

application.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    # Set webhook URL
    import requests
    WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    application.bot.set_webhook(url=WEBHOOK_URL)
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
