import telebot
import requests
from keep_alive import keep_alive

TOKEN = '7576436917:AAFkiGPj7tqfk1pgVvBh5rsVKwCRO9OvbKY'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! برای دریافت قیمت ارز دیجیتال، فقط اسمش رو به انگلیسی وارد کن. مثل: bitcoin یا ethereum")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "مثال: بنویس bitcoin یا dogecoin یا litecoin")

@bot.message_handler(func=lambda message: True)
def show_price(message):
    symbol = message.text.lower().strip()

    url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd'

    try:
        response = requests.get(url)
        data = response.json()

        if symbol in data:
            price = data[symbol]['usd']
            bot.reply_to(message, f"قیمت {symbol.capitalize()} الان: {price} دلار")
        else:
            bot.reply_to(message, 'نام ارز یافت نشد. مطمئن شو اسم کاملشو به انگلیسی وارد کردی.')
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, 'خطا در دریافت اطلاعات از.')

keep_alive()
bot.infinity_polling()