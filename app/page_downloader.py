'''Modulo page_downloader.
'''
import asyncio  # pylint: disable=import-error
import aiohttp  # pylint: disable=import-error


class PageDownloader():
    '''PageDownloader.

    Effettua il download delle urls fornite in input.
    '''

    def __init__(self):
        self.urls = []
        self.output_pages = {}

    def update_urls(self, urls):
        '''Aggiorna le urls target.
        
        Args:
            urls (list): Urls target.'''
        self.urls = urls

    def export_pages(self):
        '''Esporta le pagine scaricate.

        Returns:
            ret_val (dict): Copia del dizionario output_pages memorizzato.
        '''
        ret_val = self.output_pages.copy()
        self.output_pages.clear()
        return ret_val

    def run_fetch_loop(self):
        '''Effettua il download asincrono delle urls memorizzate.
        '''
        asyncio.run(self._get_multiple_pages())

    async def _get_multiple_pages(self):
        tasks = []
        for url in self.urls:
            tasks.append(asyncio.create_task(self._get_single_page(url)))
        await asyncio.wait(tasks, timeout=2)

    async def _get_single_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.request('get', url) as resp:
                if resp.status == 200:
                    self.output_pages[url] = await resp.text()
