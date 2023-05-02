from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    CommandHandler,
)

# First level menu
SELECTING_ACTION = "AS"
GRANT_ACCESS = "GA"

# Second level menu
SELECTING_TYPE = "ST"
USER = "SU"
CHAT = "SC"

# Shortcut for ConversationHandler.END
END = ConversationHandler.END


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
	"""End Conversation by command."""
	await update.message.reply_text("Okay, bye.")

	return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
	"""End conversation from InlineKeyboardButton."""
	await update.callback_query.answer()

	text = "See you around!"
	await update.callback_query.edit_message_text(text=text)

	return END


async def select_type(update: Update,
                      context: ContextTypes.DEFAULT_TYPE):
	print("SEL TYPE ---------------------------------")
	buttons = [
	    [
	        InlineKeyboardButton(text="USER", callback_data=USER),
	        InlineKeyboardButton(text="CHAT", callback_data=CHAT),
	    ],
	]
	keyboard = InlineKeyboardMarkup(buttons)

	await update.callback_query.answer()
	await update.callback_query.edit_message_text(
	    text="Are you looking for a user id or a chat id?",
	    reply_markup=keyboard)


async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
	await update.callback_query.answer()
	await update.callback_query.edit_message_text(text="add_user")

	return USER


async def add_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
	await update.callback_query.answer()
	await update.callback_query.edit_message_text(text="add_chat")

	return CHAT


async def permissions_grant(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> str:
	context.user_data["OPERATION"] = "GRANT"
	await select_type(update, context)
	return SELECTING_TYPE

async def permissions_menu(update: Update,
                           context: ContextTypes.DEFAULT_TYPE) -> str:
	# if await authenticate(update, context):
	text = "You can grant or revoke access to this bot to a specific user or a specific chat.\n" "To abort, simply type /stop."

	buttons = [
	    [
	        InlineKeyboardButton(text="Grant access",
	                             callback_data=GRANT_ACCESS)
	    ]
	]
	keyboard = InlineKeyboardMarkup(buttons)
	await update.message.reply_text(text=text, reply_markup=keyboard)
	return SELECTING_ACTION


def get_permission_hanler():
	return ConversationHandler(
	    entry_points=[CommandHandler("permissions", permissions_menu)],
	    states={
	        SELECTING_ACTION: [
	            CallbackQueryHandler(permissions_grant,
	                                 pattern="^" + GRANT_ACCESS + "$"),
	        ],
	        SELECTING_TYPE: [
				CallbackQueryHandler(add_user, pattern="^" + USER + "$"),
	            CallbackQueryHandler(add_chat, pattern="^" + CHAT + "$"),
			],
	    },
	    fallbacks=[CommandHandler("stop", stop)],
	)
