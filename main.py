from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

# Токен твоего бота от @BotFather
BOT_TOKEN = "8962807840:AAEX9Pnvu0xqK9jWsAXOWCn7tdK4WowtPJM"

# Telegram ID твоего друга
FRIEND_CHAT_ID = 490934292


async def forward_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    # Отправляем сообщение другу
    await update.message.copy(
        chat_id=FRIEND_CHAT_ID
    )


async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Бот будет обрабатывать обычные сообщения
    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            forward_message
        )
    )

    print("Бот запущен!")

    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())