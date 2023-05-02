import configuration
import logging
import json
from telegram import Update, Chat, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    Application,
    CallbackQueryHandler,
    ConversationHandler,
)
from modules.permissions import get_permission_hanler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# async def authenticate(update: Update, context: ContextTypes.DEFAULT_TYPE):
# 	msg = f"Access denied. Please either authorize user {update.effective_user.id} or chat {update.effective_chat.id}"
# 	await context.bot.send_message(chat_id=update.effective_chat.id,
# 								   text=msg)
# 	return False


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command.",
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(configuration.TELEGRAM_API_KEY).build()

    perm_handler = get_permission_hanler()
    application.add_handler(perm_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
