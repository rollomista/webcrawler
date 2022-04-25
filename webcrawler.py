import logging
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

TOKEN = os.getenv('API_TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG)

class Crawler:

    def __init__(self,id_msg, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.id_msg = id_msg

    def download_url(self, url):
        # download dell'intero html 
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        # parsing dell'html per ottenere nuovi riferimenti 
        soup = BeautifulSoup(html, 'html.parser')

        with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
            future_to_link = {executor.submit(soup.find_all('a', {'class':'s-access-detail-page'})): link for link in soup.find_all('a')}
            for future in concurrent.futures.as_completed(future_to_link):
                link  = future_to_link[future]
                try:
                    path = link.get('href')
                    if path and path.startswith('/'):
                        path = urljoin(url, path)
                    # self.add_url_to_visit(url)
                    self.add_url_to_visit(url)
                except Exception as exc:
                    logging.error("Expection %s", exc)



    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        # ciclo per aggiungere url parsando gli altri url

        # for url in self.get_linked_urls(url, html):
        self.get_linked_urls(url, html)
        


    def run(self):
    # def run(self):
        while self.urls_to_visit:
            # url da visitare
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')

            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)
                # await queue.put(url)
        
        logging.warning(f'Length list: {len(self.urls_to_visit)}')

    def analysis(self):
        while True:
            while self.visited_urls:
                # url = await queue.get()
                url = self.visited_urls.pop(0)
                logging.debug(f'Get url by queue {url}')

            

@bot.message_handler(commands=['hello'])
def hello(message): 
    bot.reply_to(message, "hey! i'm rollomista's crawler... try this")

@bot.message_handler(commands=['start'])
def start(message):
    # asyncio.run(main(message.chat.id))
    main(message.chat.id)

def main(id_msg):
    start = time.time()
    # queue = asyncio.Queue()
    crawler = Crawler(id_msg, urls=['https://www.unieuro.it/online/'])
    

    pidList = []

    #compute(currRange)
    pid1 = Process(target=crawler.run, args=())
    pid1.start()
    pidList.append(pid1)        
    pid2 = Process(target=crawler.analysis, args=())
    pid2.start()
    pidList.append(pid2)        
        
    for pid in pidList:
        pid.join()

    end = time.time()
    logging.info("Elapsed {0} seconds".format(end-start))

    bot.send_message(id_msg, "Il crawling è terminato: {0}".format(end-start))


if __name__ == '__main__':
    bot.polling()
