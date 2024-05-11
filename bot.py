import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


main_url = "url to server"

# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [KeyboardButton(
                text="Submit solution!",
                web_app=WebAppInfo(url=f"{main_url}?uid={update.message.from_user.id}&username={update.message.from_user.username}"),
            ),
        KeyboardButton(
            text="Show results!",
            web_app=WebAppInfo(
                url=f"{main_url}/results"),
        )
    ]
    await update.message.reply_text(
        "Привет!",
        reply_markup=ReplyKeyboardMarkup.from_row(buttons),
    )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    token = open('token.txt').readline().strip()
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
