import requests
import logging
import threading
from lxml import html
import time
import telebot
import os


TOKEN = os.getenv('API_TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG)

class AlertBot:

    def __init__(self, id_msg, url):
        self.id_msg = id_msg
        self.url = url

    def check_available(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        
        # adding headers to show that you are
        # a browser who is sending GET request
        page = requests.get(self.url, headers = headers)
        # soup = BeautifulSoup(html, 'html.parser')
        # for input in soup.find_all('input'):
        #     id = input.get('id')
        #     name = input.get('name')
        #     if id == 'buy-now-button' and name =='submit.buy-now':
        #         bot.send_message(self.id_msg, f'Disponibile -> {self.url }')
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

    def run(self):
        arr = [
            'Only 1 left in stock.',
            'Only 2 left in stock.',
            'In stock.',
            'Disponibilità immediata.']
        ans = self.check_available()
        logging.debug(ans)
        if ans in arr:
            bot.send_message(self.id_msg, f'Disponibile -> {self.url} [{ans}] ')

def alert_bot(id_msg):

    urls = ['https://www.amazon.it/Playstation-Sony-PlayStation-5/dp/B08KKJ37F7', 'https://www.amazon.it/Sony-PlayStation%C2%AE5-DualSenseTM-Wireless-Controller/dp/B09NLFPD4Q/ref=sr_1_1?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1I0ENLCB7UWGN&keywords=ps5&qid=1650915089&sprefix=ps5%2Caps%2C125&sr=8-1&th=1']
    thrList = []
    for url in urls:

        alert = AlertBot(id_msg, url)

        thr = threading.Thread(target=alert.run(), args=())
        thr.start()
        thrList.append(thr)
        
    for thr in thrList:
        thr.join()