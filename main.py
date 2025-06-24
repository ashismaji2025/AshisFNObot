from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = "7526432651:AAE0XPCvy43_KuEWfwDZPHKf1n2AQl_YiMA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello Ashis-da! Your AshisF&Obot is now active 💹")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
