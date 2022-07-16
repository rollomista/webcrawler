import logging
import os
import threading
import time
import app.alertbot as alertbot
# telegram
import telebot

import app.page_downloader as pd # pylint: disable=import-error
import app.parser as p # pylint: disable=import-error
import app.db_mediator as db # pylint: disable=import-error


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
    id_msg = message.chat.id
    while True:
        start = time.time()
        alertbot.alert_bot(message.chat.id)
        
        end = time.time()

        logging.info("alert - Elapsed {0} seconds".format(end-start))
        bot.send_message(id_msg, "Tempo alert: {0}".format(end-start))

        time.sleep(2)

@bot.message_handler(commands=['start_crawler'])
def start_crawler(message):
    
    seed_urls = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/']
    words = ['Biden', 'COVID', 'Putin', 'lockdown', 'information', 'data']
    id_msg = message.chat.id

    downloader = pd.PageDownloader()
    parser = p.Parser()
    db_mediator = db.DbMediator()
    db_mediator.connect()

    iter = 0
    while True:
        start = time.time()
        downloader.update_urls(seed_urls)
        downloader.run_fetch_loop()
        pages = downloader.export_pages()

        parser.update_pages(pages)
        seed_urls = parser.extract_output_urls()
        word_count_table = parser.count_word_instances(words)

        db_mediator.update_word_tables(word_count_table)
        db_mediator.print_word_table(words[0])

        end = time.time()
        logging.info("crawler - Elapsed {0} seconds".format(end-start))

        bot.send_message(id_msg, str(iter) + " - crawling elapsed: {0} seconds".format(end-start))
        iter += 1


if __name__ == '__main__':
    logging.info("Start bot")
    bot.polling()

 
