import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Вставь сюда токен от @BotFather
TOKEN = "8962807840:AAEX9Pnvu0xqK9jWsAXOWCn7tdK4WowtPJM"

# Часовой пояс Тбилиси
TIMEZONE = ZoneInfo("Asia/Tbilisi")

# Здесь бот будет хранить ID пользователя
chat_id = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id

    chat_id = update.effective_chat.id

    await update.message.reply_text(
        "Готово! Я запомнил этот чат.\n"
        "Буду отправлять «ТАБЛЕТКИ» каждые 30 минут с 20:00 до 00:00."
    )


async def reminder():
    global chat_id

    while True:
        now = datetime.now(TIMEZONE)

        # Сегодняшние времена отправки:
        # 20:00, 20:30, 21:00 ... 23:30, 00:00

        if now.hour < 4:
            target = now.replace(
                hour=4, minute=0, second=0, microsecond=0
            )

        elif now.hour >= 4:
            # Находим ближайшее время, кратное 30 минутам
            minute = 0 if now.minute < 30 else 30

            target = now.replace(
                minute=minute,
                second=0,
                microsecond=0
            )

            # Если это время уже прошло — берём следующие 30 минут
            if target <= now:
                target += timedelta(minutes=30)

            # После полуночи следующий цикл начинается в 20:00
            if target.hour == 0:
                # 00:00 является последним сообщением
                pass

        else:
            target = now

        # Если сейчас уже после 00:00, ждём до 20:00
        if now.hour == 0 and now.minute > 0:
            target = (now + timedelta(days=1)).replace(
                hour=4, minute=0, second=0, microsecond=0
            )

        wait_seconds = (target - now).total_seconds()

        if wait_seconds > 0:
            await asyncio.sleep(wait_seconds)

        # Отправляем сообщение
        if chat_id is not None:
            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text="ТАБЛЕТКИ"
                )
            except Exception as e:
                print("Ошибка отправки:", e)

        # Если отправили в 00:00 — ждём до 20:00
        if target.hour == 0 and target.minute == 0:
            tomorrow = target + timedelta(days=1)
            next_target = tomorrow.replace(
                hour=20, minute=0, second=0, microsecond=0
            )

            await asyncio.sleep(
                (next_target - datetime.now(TIMEZONE)).total_seconds()
            )


async def main():
    global bot

    application = Application.builder().token(TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    bot = application.bot

    # Запускаем напоминания параллельно с ботом
    asyncio.create_task(reminder())

    print("Бот запущен!")

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Бесконечная работа
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
  