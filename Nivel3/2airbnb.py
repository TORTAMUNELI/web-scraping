from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Instalar automaticamente el driver de Chrome
from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
)
# opts.add_argument("--headless") # Headless Mode


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=opts)

# Alternativamente (Hay que tener el driver actualizado de Chrome):
# driver = webdriver.Chrome(
#     service=Service('./chromedriver'),
#     options=opts
# )

driver.get("https://www.airbnb.com.co/")
sleep(5)

titulos_anuncios = driver.find_elements(By.XPATH, '//div[@data-testid="listing-card-title"]')
for titulo in titulos_anuncios:
    print(titulo.text)
