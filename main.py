import asyncio
from datetime import time
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# =========================
# НАСТРОЙКИ
# =========================

BOT_TOKEN = "8715730941:AAH7bXZmypIUoPCUJ8sWTYjCacbwKX30Xcg"

# Сюда впиши Telegram ID пользователя,
# которому нужно отправлять сообщения.
TARGET_USER_ID = 490934292

TIMEZONE = ZoneInfo("Asia/Tbilisi")


# =========================
# КОМАНДЫ
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Бот запущен. Я буду присылать напоминания по расписанию."
    )


# =========================
# ОТПРАВКА НАПОМИНАНИЯ
# =========================

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=TARGET_USER_ID,
        text="ТАБЛЕТКИ"
    )


# =========================
# ЗАПУСК
# =========================

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Первое сообщение — в 20:00.
    app.job_queue.run_daily(
        send_reminder,
        time=time(20, 0, tzinfo=TIMEZONE),
    )

    # Остальные сообщения каждые 30 минут:
    # 20:30, 21:00, 21:30 ... 23:30, 00:00
    for hour in range(20, 24):
        for minute in (30,):
            if hour == 23 and minute == 30:
                continue

            app.job_queue.run_daily(
                send_reminder,
                time=time(hour, minute, tzinfo=TIMEZONE),
            )

    # Полночь
    app.job_queue.run_daily(
        send_reminder,
        time=time(0, 0, tzinfo=TIMEZONE),
    )

    print("Бот запущен!")
    print("Напоминания: с 20:00 до 00:00 каждые 30 минут.")

    app.run_polling()


if __name__ == "__main__":
    main()
