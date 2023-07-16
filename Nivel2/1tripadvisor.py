from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()


class TripAdvisorCS(CrawlSpider):
    name = 'Hoteles'
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    start_urls = ['https://www.tripadvisor.co/Hotels-g676524-Villa_de_Leyva_Boyaca_Department-Hotels.html']
    # Tiempo entre requerimientos
    download_delay = 2
    rules = (
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'
            ),
            follow=True,
            callback="parse_hotel"
        ),
    )

    def hacerMayusculas(self, texto):
        return texto.upper()

    def parse_hotel(self, response, **kwargs):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()', MapCompose(self.hacerMayusculas))
        #item.add_xpath('precio', '(//div[@class="WXMFC b"])[1]/text()')
        #item.add_xpath('descripcion', '//div[@class="fIrGe _T"][1]/text()')
        #item.add_xpath('amenities', '//div[contains(@data-test-target, "amenity_text")]/text()')

        yield item.load_item()
