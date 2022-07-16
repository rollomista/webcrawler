'''Modulo parser.
'''
import bs4 as bs  # pylint: disable=import-error


class Parser():
    '''Parser.

    Processa le input_pages per estrarre nuove urls e informazioni utili.
    '''

    def __init__(self):
        self.parsed_pages = {}

    def update_pages(self, input_pages):
        '''Aggiorna le pagine da parsare.

        Aggiorna la variabile di istanza parsed_pages (dict),
        che usa delle urls come keys e degli oggetti bs4.BeautifulSoup come values

        Args:
            input_pages (dict): Dizionario che usa delle urls come keys e
            delle string contenenti l'html della pagina come values
        '''
        for input_url in input_pages:
            self.parsed_pages[input_url] = bs.BeautifulSoup(
                input_pages.get(input_url), 'html.parser')

    def extract_output_urls(self):
        '''Estrae una lista di ulrs (lunghezza massima = 20) dalle parsed_pages.

        Returns:
            ret_urls (list): Lista di urls
        '''
        tmp_urls = []
        max_urls = 20
        ret_urls = []

        for parsed_page in self.parsed_pages.values():
            for link in parsed_page.find_all('a'):
                tmp = link.get('href')
                if isinstance(tmp, str) and tmp.startswith('https'):
                    tmp_urls.append(tmp)
        cnt = 0
        step = len(tmp_urls)//max_urls
        while cnt < max_urls:
            ret_urls.append(tmp_urls[cnt*step])
            cnt += 1
        return ret_urls

    def count_word_instances(self, words):
        '''Conta il numero di occorrenze delle parole words in ciascuna delle parsed pages.

        Args:
            word (list): Lista di parole da ricercare.
        Returns:
            ret_table (dict): Dizionario con keys uguali alle words
            e values uguali ad una lista di tuples (parsed_url, word_count).
        '''
        ret_table = {}

        for word in words:
            ret_table[word] = []

        for parsed_url in self.parsed_pages:
            for word in words:
                parsed_page = self.parsed_pages.get(parsed_url)
                parsed_page_text = parsed_page.get_text()
                word_count = parsed_page_text.count(word)
                ret_table.get(word).append((parsed_url, word_count))
        return ret_table
