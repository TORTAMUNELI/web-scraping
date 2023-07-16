from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Aritculo(Item):
    titulo = Field()
    precio = Field()
    desc = Field()


class MercadoLibreCS(CrawlSpider):
    name = 'Mercado Libre CrawlSpider'
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "CLOSESPIDER_PAGECOUNT": 55,
        "FEED_EXPORT_FIELDS": ["titulo", "precio", "desc"]
    }
    # download_delay = 1
    start_urls = ['https://listado.mercadolibre.com.co/celular']
    allowed_domains = ["listado.mercadolibre.com.co", "mercadolibre.com.co"]
    rules = (
        # Paginacion
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[contains(@class,"andes-pagination__button--next")]/a'))),
        # Detalle de los productos
        Rule(
            LinkExtractor(allow=(), restrict_xpaths=(
                '//li[@class="ui-search-layout__item shops__layout-item"]//div[contains(@class,"ui-search-result__content-wrapper")]//a[contains(@class,"ui-search-item__group__element")]')),
            follow=True,
            callback="parse_articulo"
        ),
    )

    def parse_articulo(self, response):
        sel = Selector(response)
        item = ItemLoader(Aritculo(), sel)
        item.add_xpath('titulo', '//h1[@class="ui-pdp-title"]/text()')
        item.add_xpath('desc', 'string(//p[contains(@class, "ui-pdp-description")])')
        item.add_xpath('precio', '(//span[@class="andes-money-amount__fraction"]/text())[1]')
        yield item.load_item()
