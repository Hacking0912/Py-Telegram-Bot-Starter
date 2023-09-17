# Path: main.py
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from keep_alive import keep_alive
# Telegram bot token and username
TOKEN: Final = 'YOUR_TELEGRAM_BOT_TOKEN'
BOT_USERNAME: Final = 'YOUR_TELEGRAM_BOT_USERNAME'

# Start the Flask server in a separate thread
keep_alive()

# Command handler for the '/start' command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello thanks for chatting with me! I am {BOT_USERNAME}!')

# Command handler for the '/help' command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = "This is a help message for your bot. You can provide instructions or information about the available commands here."
    await update.message.reply_text(help_message)

# Message response logic, you can replace this with your own logic or API call
async def message_response(text: str):
    if text == 'hello':
        return 'Hello there!'
    if text == 'hi':
        return 'Hi there!'
    else:
        return 'Sorry, I don\'t understand you.'

# Message handler for handling user messages
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    # Check if the message is a group message or a private message
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            await update.message.chat.send_action('typing')
            response = await message_response(new_text)
            await update.message.reply_text(response)
    # If the message is a private message
    if message_type == 'private':
        response = await message_response(text)
        await update.message.chat.send_action('typing')
        await update.message.reply_text(response)

# Error handler for handling any errors that occur during bot execution
def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"An error occurred: {context.error}")
# Main function
if __name__ == '__main__':
    print('Polling...')
    app = Application.builder().token(TOKEN).build()# Create the Application instance
    app.add_handler(CommandHandler('start', start_command))# Add the handlers for the '/start' and '/help' commands
    app.add_handler(CommandHandler('help', help_command))# Add the handler for the message handler
    app.add_handler(MessageHandler(filters.TEXT, message_handler))# Add the error handler
    app.add_error_handler(error_handler)  # Add the error handler
    app.run_polling()# Start the polling loop
