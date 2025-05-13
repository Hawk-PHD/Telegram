import telebot
import requests
from keep_alive import keep_alive

TOKEN = '7763235408:AAH6kHMOmqWLD-dm_zt_PBSjDg2mVrp8ki8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! برای دریافت قیمت ارز دیجیتال، فقط اسمش رو به انگلیسی وارد کن. مثل: bitcoin یا ethereum")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "مثال: بنویس bitcoin یا dogecoin یا litecoin")

@bot.message_handler(func=lambda message: True)
def show_price(message):
    symbol_input = message.text.lower().strip()

    if not symbol_input:
        bot.reply_to(message, "اسم ارز نمی‌تونه خالی باشه.")
        return

    url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol_input}&vs_currencies=usd'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    print(f"Final URL: {url}")

    try:
        response = requests.get(url, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")

        if response.status_code == 200:
            data = response.json()
            if symbol_input in data:
                price = data[symbol_input]['usd']
                bot.reply_to(message, f"قیمت {symbol_input} الان: {price} دلار")
            else:
                bot.reply_to(message, "نام ارز پیدا نشد.")
        else:
            bot.reply_to(message, f"پاسخ نامعتبر از سرور: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"خطا: {e}")
        print(f"Error: {e}")
keep_alive()
bot.infinity_polling()
