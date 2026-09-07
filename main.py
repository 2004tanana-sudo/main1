"""
Telegram-бот для двух человек: всё, что пишет один, пересылается другому.

Установка:
    pip install python-telegram-bot --upgrade

Запуск:
    python relay_bot.py

Перед запуском заполните ниже:
    BOT_TOKEN — токен бота от @BotFather
    USER_1_ID, USER_2_ID — числовые Telegram ID вас и девушки

Как узнать свой ID:
    напишите боту @userinfobot — он пришлёт ваш числовой ID.
"""

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

# ==== НАСТРОЙКИ ====
BOT_TOKEN = "8962807840:AAEX9Pnvu0xqK9jWsAXOWCn7tdK4WowtPJM"
USER_1_ID = 934199724  # ваш Telegram ID
USER_2_ID = 490934292  # ID девушки
# ====================

ALLOWED_IDS = {USER_1_ID, USER_2_ID}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def get_partner_id(user_id: int) -> int | None:
    """Возвращает ID второго участника переписки."""
    if user_id == USER_1_ID:
        return USER_2_ID
    if user_id == USER_2_ID:
        return USER_1_ID
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in ALLOWED_IDS:
        await update.message.reply_text("Извините, этот бот приватный.")
        return
    await update.message.reply_text(
        "таблетки."
    )


async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    # Проверка доступа — реагируем только на двух разрешённых пользователей
    if user_id not in ALLOWED_IDS:
        logger.info("Заблокирован доступ для user_id=%s", user_id)
        return

    partner_id = get_partner_id(user_id)
    if partner_id is None:
        return

    message = update.message

    try:
        # Пересылаем оригинальное сообщение (текст, фото, стикеры, голосовые и т.д.)
        await context.bot.copy_message(
            chat_id=partner_id,
            from_chat_id=update.effective_chat.id,
            message_id=message.message_id,
        )
    except Exception as e:
        logger.error("ERROR: %s", e)
        await message.reply_text(
            "Не получилось отправить сообщение. Возможно, второй человек ещё не запускал бота (/start)."
        )


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    # ALL — ловим любые типы сообщений: текст, фото, видео, голосовые, стикеры и т.д.
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, relay))

    logger.info("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()