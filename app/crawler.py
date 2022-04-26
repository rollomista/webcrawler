import logging
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import telebot
import os
import time
import app.myqueue as myqueue
import threading


TOKEN = os.getenv('API_TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG)


class Crawler:

    def __init__(self,id_msg, queue, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.id_msg = id_msg
        self.queue = queue

    def download_url(self, url):
        # download dell'intero html 
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        # parsing dell'html per ottenere nuovi riferimenti 
        soup = BeautifulSoup(html, 'html.parser')

        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit and url is not None:
            self.queue.add_item(url)
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        # ciclo per aggiungere url parsando gli altri url

        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)
        
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
        print("QUAAAAAAAAAAAAAAAAAAAAAAAAAAA-----------------------")
        url = self.queue.consume_item()
        logging.debug(f'Get url by queue {url}')

def crawler_bot(id_msg):
    thrList = []

    queue = myqueue.MyQueue()
    crawler = Crawler(id_msg, queue, urls=['https://www.amazon.com/'])

    thr2 = threading.Thread(target=crawler.analysis(), args=())

    thr1 = threading.Thread(target=crawler.run(), args=())
    print("OOOOOOOOOOOOOOO")
    thr2.start()
    time.sleep(2)
    thr1.start()


    for thr in thrList:
        thr.join()
    