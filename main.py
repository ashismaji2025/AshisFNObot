import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load the bot token from environment variables
TOKEN = os.environ.get("BOT_TOKEN")

# Define a start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Ashis-da! 💹 Your AshisFNObot is now working 💖")

def main():
    # Create the bot application
    app = ApplicationBuilder().token(TOKEN).build()

    # Add a simple /start command handler
    app.add_handler(CommandHandler("start", start))

    # Start polling
    app.run_polling()

if __name__ == "__main__":
    main()
