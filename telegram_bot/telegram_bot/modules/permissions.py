from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    CommandHandler,
)

# Meta states
STOPPING, SHOWING = map(chr, range(0, 2))

# First level menu
SELECTING_ACTION = map(chr, range(2, 3))
GRANT_ACCESS, REVOKE_ACCESS = map(chr, range(3, 5))

# Shortcut for ConversationHandler.END
END = ConversationHandler.END

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
    await update.message.reply_text("Okay, bye.")

    return END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End conversation from InlineKeyboardButton."""
    await update.callback_query.answer()

    text = "See you around!"
    await update.callback_query.edit_message_text(text=text)

    return END

async def permissions_grant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
	
    await context.bot.send_message(chat_id=update.effective_chat.id, text="GRANT WIP")
    return GRANT_ACCESS


async def permissions_revoke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="REVOKE WIP")
    return REVOKE_ACCESS


async def permissions_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    # if await authenticate(update, context):
    text = (
        "You can grant or revoke access to this bot to a specific user or a specific chat.\n"
        "To abort, simply type /stop."
    )

    buttons = [
        [
            InlineKeyboardButton(text="Grant access", callback_data=str(GRANT_ACCESS)),
            InlineKeyboardButton(
                text="Revoke access", callback_data=str(REVOKE_ACCESS)
            ),
        ],
        [
            InlineKeyboardButton(text="Done", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(text=text, reply_markup=keyboard)
    return SELECTING_ACTION


def get_permission_hanler():
    return ConversationHandler(
        entry_points=[CommandHandler("permissions", permissions_menu)],
        states={
            SHOWING: [
                CallbackQueryHandler(permissions_menu, pattern="^" + str(END) + "$")
            ],
            SELECTING_ACTION: [
                CallbackQueryHandler(
                    permissions_grant, pattern="^" + str(GRANT_ACCESS) + "$"
                ),
                CallbackQueryHandler(
                    permissions_revoke, pattern="^" + str(REVOKE_ACCESS) + "$"
                ),
                CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
            ],
            GRANT_ACCESS: [CommandHandler("permissions", permissions_menu)],  # TODO
            REVOKE_ACCESS: [CommandHandler("permissions", permissions_menu)],  # TODO
        },
        fallbacks=[CommandHandler("stop", stop)]
    )
