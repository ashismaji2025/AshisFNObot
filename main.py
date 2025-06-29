from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace with your actual bot token
TOKEN = "7526432651:AAGpowkLKalWPw2w9pjzp5Hm3G797DS9p74"

# Define the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! Your AshisFNObot is now active 💹")

# Main entry point
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()  # <-- This is where .run_polling() is used

if __name__ == "__main__":
    main()
