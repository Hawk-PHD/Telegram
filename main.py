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

    url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol_input}&vs_currencies=usd'
    print(f"Final URL: {url}")  # چاپ لینک نهایی برای بررسی

    try:
        response = requests.get(url)

        # بررسی اینکه آیا پاسخ معتبره
        if response.status_code != 200:
            bot.reply_to(message, f"پاسخ نامعتبر از سرور (status {response.status_code})")
            print(f"Bad response: {response.text}")
            return

        # بررسی اینکه آیا JSON قابل پردازشه
        try:
            data = response.json()
        except Exception as e:
            bot.reply_to(message, f'خطا در تبدیل داده: {e}')
            print(f"Raw text: {response.text}")
            return

        if symbol_input in data:
            price = data[symbol_input]['usd']
            bot.reply_to(message, f"قیمت {symbol_input.capitalize()} الان: {price} دلار")
        else:
            bot.reply_to(message, 'ارز پیدا نشد. لطفاً اسم کامل انگلیسی مثل bitcoin بنویس.')

    except Exception as e:
        bot.reply_to(message, f'خطا: {e}')
        print(f"Error: {e}")
keep_alive()
bot.infinity_polling()
