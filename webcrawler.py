import logging
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# telegram
import telebot

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
        # posso parallellizzare la ricerca? - ricerca di nuovi link e check della pagina se è presente cosa? mmm
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path


    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        # ciclo per aggiungere url parsando gli altri url
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)


    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            #invio
            bot.send_message(self.id_msg, f'Crawling: {url}')

            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)



@bot.message_handler(commands=['Greet'])
def greet(message): 
    bot.reply_to(message, "Hey, i'm rollo crawler")

@bot.message_handler(commands=['hello'])
def hello(message): 
    bot.send_message(message.chat.id, "Hi!:)")

@bot.message_handler(commands=['start'])
def start(message):
    Crawler(message.chat.id, urls=['https://www.amazon.com/']).run()


if __name__ == '__main__':
    bot.polling()
