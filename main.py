import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get your bot token from environment variable
TOKEN = os.environ.get("BOT_TOKEN")

# Define a simple /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! 🤖 AshisFNObot is now live and working!")

# Main function to start the bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

# Entry point
if __name__ == "__main__":
    main()
