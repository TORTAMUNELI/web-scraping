import requests
from lxml import html

url = 'https://www.wikipedia.org/'

encabezados = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=encabezados)
parser = html.fromstring(response.text)

#idiomas = parser.xpath("//div[contains(@class, 'central-featured-lang')]//strong/text()")
#for idioma in idiomas:
#    print(idioma)

idiomas = parser.find_class('central-featured-lang')
for idioma in idiomas:
    print(idioma.text_content())