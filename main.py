import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

# Get token from Render environment variable
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Bot is now live on Render! 😊")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
