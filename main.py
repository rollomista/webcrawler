import logging
import os
import threading
import time
import app.alertbot as alertbot
import app.crawler as crawler
import app.myqueue as queue
# telegram
import telebot



TOKEN = os.getenv('API_TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG)



@bot.message_handler(commands=['hello'])
def hello(message): 
    bot.reply_to(message, "hey! i'm a crawler... try this")

@bot.message_handler(commands=['start_alert'])
def start_alert(message):
    while True:
        alertbot.alert_bot(message.chat.id)
        time.sleep(1)

@bot.message_handler(commands=['start_crawler'])
def start_crawler(message):
    start = time.time()
    id_msg = message.chat.id
    crawler.crawler_bot(id_msg)
    end = time.time()
    logging.info("Elapsed {0} seconds".format(end-start))

    bot.send_message(id_msg, "Il crawling è terminato: {0}".format(end-start))


if __name__ == '__main__':
    logging.info("Start bot")
    bot.polling()

 
