import os
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or "your-token-here"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") or "https://ashisfnobot.onrender.com/webhook"

bot = Bot(token=TOKEN)
app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is now active 💹")

application.add_handler(CommandHandler("start", start))

@app.route('/webhook', methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put(update)
    return "ok"

@app.route('/')
def home():
    return "AshisFNObot is running..."

if __name__ == '__main__':
    application.initialize()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
