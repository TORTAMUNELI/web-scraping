from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess


class Noticia(Item):
    titular = Field()
    # descripcion = Field()


class UniversoSpider(Spider):
    name = "SegundoSpider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    start_urls = ["https://www.eluniverso.com/deportes/"]

    def parse(self, response, **kwargs):
        sel = Selector(response)
        noticias = sel.xpath("//ul[contains(@class, 'feed')]/li/div[contains(@class, 'story')]")
        for noticia in noticias:
            item = ItemLoader(Noticia(), noticia)
            item.add_xpath('titular', './/h2/a/text()')

            yield item.load_item()

    # Ejemplo con BeautifulSoup (No funciona)
    """
    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.body)
        contenedor_noticias = soup.find_all('etiqueta', class_='clase')
        for contenedor in contenedor_noticias:
            #El recursive lo que hace es buscar entre cualquier hijo
            noticias = contenedor.find_all('etiqueta', class_="clase", recursive=False)
            for noticia in noticias:
                item = ItemLoader(Noticia, response.body)
                titular = noticia.find('etiqueta', class_="clase")
                
                if (titular != None):
                    titular = titular.text
                else:
                    titular = N/A
                
                item.add_value('titular', titular)
                yield item.load_item()
    """


#scrapy runspider .\eluniverso_scrappy.py -o noticias.csv -t csv
# Ejecutar sin la necsidad de terminal
process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'noticias.csv'
})
process.crawl(UniversoSpider)
process.start()
