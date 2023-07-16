from scrapy.item import Field, Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


class Pregunta(Item):
    id = Field()
    pregunta = Field()
    #descripcion = Field()


# Spider es para la extracción de una sola página
class StackOverflowSpider(Spider):
    name = "PrimerSpider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    start_urls = ['https://stackoverflow.com/questions']

    def parse(self, response, **kwargs):
        sel = Selector(response)
        preguntas = sel.xpath("//div[@id='questions']//div[contains(@class, 's-post-summary')]")
        for pregunta in preguntas:
            item = ItemLoader(Pregunta(), pregunta)
            item.add_xpath('pregunta', './/h3/a/text()')
            #item.add_xpath('descripcion', ".//div[@class='excerpt']/text()")
            item.add_value('id', 1)
            yield item.load_item()

#scrapy runspider .\stackoverflow_scrappy.py -o noticias.csv -t csv