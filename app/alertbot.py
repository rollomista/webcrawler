import requests
import logging
import threading
from lxml import html
import time
import os
import telebot
from bs4 import BeautifulSoup



TOKEN = os.getenv('API_TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG)

class AlertBot:

    def __init__(self, id_msg):
        self.id_msg = id_msg

    def check_available(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        
        # adding headers to show that you are
        # a browser who is sending GET request
        page = requests.get(url, headers = headers)

        for _ in range(20):
            # because continuous checks in
            # milliseconds or few seconds
            # blocks your request
            time.sleep(3)
            
            # parsing the html content
            doc = html.fromstring(page.content)
        
        # checking availability
            XPATH_AVAILABILITY = '//div[@id ="availability"]//text()'
            raw_availability = doc.xpath(XPATH_AVAILABILITY)
            AVAILABILITY = ''.join(raw_availability).strip() if raw_availability else None
            return AVAILABILITY

    def run(self, url):
        arr = [
            'Only 1 left in stock.',
            'Only 2 left in stock.',
            'In stock.',
            'Disponibilità immediata.']
        ans = self.check_available(url)
        logging.debug(ans)
        if ans in arr:
            bot.send_message(self.id_msg, f'Disponibile -> {url} [{ans}] ')

def alert_bot(id_msg):

    urls_book = open('urls.csv', 'r')
    urls = urls_book.readlines()

    thrList = []

    for line in urls:
        url = line.strip()
        if url != None and isinstance(url, str):
            logging.info(f'alert url: {url}')
            # alert = AlertBot(id_msg, url)

            thr = threading.Thread(target=AlertBot(id_msg).run, args=(url, ))
            thr.start()
            thrList.append(thr)

    for thr in thrList:
        thr.join()

        