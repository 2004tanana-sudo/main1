import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters


# =========================
# НАСТРОЙКИ
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "8962807840:AAEX9Pnvu0xqK9jWsAXOWCn7tdK4WowtPJM")

YOUR_ID = 934199724          # Твой Telegram ID
GIRLFRIEND_ID = 490934292   # Telegram ID девушки


# =========================
# ПЕРЕСЫЛКА СООБЩЕНИЙ
# =========================

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user

    # Если сообщения нет — ничего не делаем
    if message is None or user is None:
        return

    # Разрешаем отправку только тебе
    if user.id != YOUR_ID:
        return

    # Пересылаем сообщение девушке
    try:
        await message.forward(
            chat_id=GIRLFRIEND_ID
        )
    except Exception as e:
        print(f"Ошибка при пересылке: {e}")


# =========================
# ЗАПУСК БОТА
# =========================

def main():
    if BOT_TOKEN == "ВСТАВЬ_ТОКЕН_БОТА_СЮДА":
        raise ValueError("Вставь токен бота в BOT_TOKEN")

    app = Application.builder().token(BOT_TOKEN).build()

    # Обрабатываем любые сообщения
    app.add_handler(
        MessageHandler(
            filters.ALL,
            forward_message
        )
    )

    print("Бот запущен.")
    print(f"Твой ID: {YOUR_ID}")
    print(f"ID девушки: {GIRLFRIEND_ID}")

    app.run_polling()


if __name__ == "__main__":
    main()