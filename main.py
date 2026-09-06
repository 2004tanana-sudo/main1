import os, requests, telebot

bot = telebot.TeleBot(os.getenv("7706743761:AAHO3-x0EZ-TTETMq5obr-OhKRzQhjqkFY0"))
STEAM_ID = "76561198335549730"

@bot.message_handler(commands=["MMR"])
def mmr(m):
    d = requests.get(f"https://api.opendota.com/api/players/{STEAM_ID}").json()
    bot.reply_to(m, f"MMR: {d['mmr_estimate']['estimate']}")

bot.infinity_polling()