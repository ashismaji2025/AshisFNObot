import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Use environment variable or directly paste token here (for testing only)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PASTE_YOUR_TOKEN_HERE")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis‑da! Your AshisFNObot is active 💹")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
