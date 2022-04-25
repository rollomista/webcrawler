import logging
import multiprocessing
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# telegram
import telebot

# threading / multiprocessing
import time
import threading
from multiprocessing import Process
import asyncio
import concurrent.futures

# amazon.
from lxml import html
import schedule
import smtplib


TOKEN = os.getenv('API_TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG)

# class Crawler:

#     def __init__(self,id_msg, urls=[]):
#         self.visited_urls = []
#         self.urls_to_visit = urls
#         self.id_msg = id_msg

#     def download_url(self, url):
#         # download dell'intero html 
#         return requests.get(url).text

#     def get_linked_urls(self, url, html):
#         # parsing dell'html per ottenere nuovi riferimenti 
#         soup = BeautifulSoup(html, 'html.parser')

#         for link in soup.find_all('a'):
#             path = link.get('href')
#             if path and path.startswith('/'):
#                 path = urljoin(url, path)
#             # self.add_url_to_visit(url)
#             self.add_url_to_visit(url)


#         # with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
#         #     future_to_link = {executor.submit(soup.find_all('a', {'class':'s-access-detail-page'})): link for link in soup.find_all('a')}
#         #     for future in concurrent.futures.as_completed(future_to_link):
#         #         link  = future_to_link[future]
#         #         try:
#         #             path = link.get('href')
#         #             if path and path.startswith('/'):
#         #                 path = urljoin(url, path)
#         #             # self.add_url_to_visit(url)
#         #             self.add_url_to_visit(url)
#         #         except Exception as exc:
#         #             logging.error("Expection %s", exc)



#     def add_url_to_visit(self, url):
#         if url not in self.visited_urls and url not in self.urls_to_visit:
#             self.urls_to_visit.append(url)

#     def crawl(self, url):
#         html = self.download_url(url)
#         # ciclo per aggiungere url parsando gli altri url

#         # for url in self.get_linked_urls(url, html):
#         self.get_linked_urls(url, html)
        


#     def run(self):
#     # def run(self):
#         while self.urls_to_visit:
#             # url da visitare
#             url = self.urls_to_visit.pop(0)
#             logging.info(f'Crawling: {url}')

#             try:
#                 self.crawl(url)
#             except Exception:
#                 logging.exception(f'Failed to crawl: {url}')
#             finally:
#                 self.visited_urls.append(url)
#                 # await queue.put(url)
        
#         logging.warning(f'Length list: {len(self.urls_to_visit)}')

#     def analysis(self):
#         while True:
#             while self.visited_urls:
#                 # url = await queue.get()
#                 url = self.visited_urls.pop(0)
#                 logging.debug(f'Get url by queue {url}')


class AlertBot:

    def __init__(self, id_msg, url):
        self.id_msg = id_msg
        self.url = url

    # def download_url(self, url):
    #     # download dell'intero html 
    #     return requests.get(url).text

    # def get_linked_urls(self, html):
    #     # parsing dell'html per ottenere nuovi riferimenti 
    #     soup = BeautifulSoup(html, 'html.parser')

    #     for input in soup.find_all('input'):
    #         id = input.get('id')
    #         name = input.get('name')
    #         if id == 'buy-now-button' and name =='submit.buy-now':
    #             bot.send_message(self.id_msg, f'Disponibile -> {self.url }')
    # def crawl(self):
    #     html = self.download_url(self.url)
    #     # ciclo per aggiungere url parsando gli altri url

    #     # for url in self.get_linked_urls(url, html):
    #     self.get_linked_urls(html)
    
    def check_available(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        # adding headers to show that you are
        # a browser who is sending GET request
        page = requests.get(self.url, headers = headers)
        for _ in range(20):
            # because continuous checks in
            # milliseconds or few seconds
            # blocks your request
            time.sleep(3)
            
            # parsing the html content
            doc = html.fromstring(page.content)
            
            # checking availability
            XPATH_AVAILABILITY = '//div[@id ="availability"]//text()'
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
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





@bot.message_handler(commands=['hello'])
def hello(message): 
    bot.reply_to(message, "hey! i'm rollomista's crawler... try this")

@bot.message_handler(commands=['start'])
def start(message):
    # asyncio.run(main(message.chat.id))
 
    # schedule.every(1).minutes.do(main(message.chat.id))
    while True:
        # running all pending tasks/jobs

        # schedule.run_pending()
        main(message.chat.id)
        time.sleep(1)

def main(id_msg):
    # queue = asyncio.Queue()
    # crawler = Crawler(id_msg, urls=['https://www.unieuro.it/online/'])
    # url = "http://www.amazon.in/dp/" + Asin

    # crawler.run()
    urls = ['https://www.amazon.it/Playstation-Sony-PlayStation-5/dp/B08KKJ37F7', 'https://www.amazon.it/Sony-PlayStation%C2%AE5-DualSenseTM-Wireless-Controller/dp/B09NLFPD4Q/ref=sr_1_1?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1I0ENLCB7UWGN&keywords=ps5&qid=1650915089&sprefix=ps5%2Caps%2C125&sr=8-1&th=1']
    # alert.crawl()

    thrList = []
    start = time.time()

    for url in urls:
        #download(url)
        alert = AlertBot(id_msg, url)
        # alert.crawl()
        thr = threading.Thread(target=alert.run(), args=())
        thr.start()
        thrList.append(thr)
        
    for thr in thrList:
        thr.join()

    end = time.time()
    logging.info("Elapsed {0} seconds".format(end-start))

    bot.send_message(id_msg, "Il crawling è terminato: {0}".format(end-start))





if __name__ == '__main__':
    logging.info("Start bot")
    bot.polling()

 
