from ast import arg
import logging
import multiprocessing
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import telebot
import os
import time
import app.myqueue as myqueue
import threading
from xlwt import *

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
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit and url != None:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        # ciclo per aggiungere url parsando gli altri url
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)
        
    def run(self):
        workbook = Workbook(encoding = 'utf-8')
        table = workbook.add_sheet('data')
        table.write(0, 0, 'url')
        line = 0
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
                # self.queue.add_item(url)
                line += 1
                table.write(line, 0, url)

                workbook.save('urls.xls')

        logging.warning(f'Length list: {len(self.urls_to_visit)}')
        

def crawler_bot(id_msg):

    # queue = myqueue.MyQueue()

    crawler = Crawler(id_msg, urls=['https://www.amazon.com/'])

    crawler.run()


    