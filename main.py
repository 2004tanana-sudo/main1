import asyncio
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from telegram import Bot

# ==================================================
# НАСТРОЙКИ
# ==================================================

TOKEN = "8715730941:AAH7bXZmypIUoPCUJ8sWTYjCacbwKX30Xcg"
TARGET_USER_ID = 490934292

TZ = ZoneInfo("Asia/Tbilisi")

MESSAGE = "ТАБЛЕТКИ"


# ==================================================
# ОСНОВНОЙ ЦИКЛ
# ==================================================

async def main():
    bot = Bot(token=TOKEN)

    print("Бот запущен.")
    print(f"ID получателя: {TARGET_USER_ID}")
    print("Расписание: с 20:00 до 00:00 каждые 30 минут.")

    last_sent = None

    while True:
        now = datetime.now(TZ)

        # Отправляем в:
        # 20:00
        # 20:30
        # 21:00
        # ...
        # 23:30
        # 00:00

        current_minutes = now.hour * 60 + now.minute

        # 20:00–23:30
        in_evening = 20 * 60 <= current_minutes <= 23 * 60 + 30

        # Ровно 00:00
        is_midnight = now.hour == 0 and now.minute == 0

        correct_time = (
            (in_evening and now.minute in (0, 30))
            or is_midnight
        )

        if correct_time and now.second < 5:
            send_key = now.strftime("%Y-%m-%d %H:%M")

            # Защита от повторной отправки
            if send_key != last_sent:
                try:
                    await bot.send_message(
                        chat_id=TARGET_USER_ID,
                        text=MESSAGE
                    )

                    print(f"[{now.strftime('%H:%M:%S')}] Отправлено: {MESSAGE}")
                    last_sent = send_key

                except Exception as e:
                    print("Ошибка отправки:", e)

        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
