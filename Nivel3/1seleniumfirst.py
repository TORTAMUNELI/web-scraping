import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Asi podemos setear el user-agent en selenium
opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome(service=Service('../chromedriver_win32/chromedriver.exe'),
                          options=opts)  # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER

# Voy a la pagina que requiero
driver.get('https://www.olx.com.ar/autos_c378')
sleep(3)
driver.refresh()  # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh o al darle click a algun elemento
sleep(5)  # Esperamos que cargue el boton
# Busco el boton para cargar mas informacion
boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
for i in range(3):  # Voy a darle click en cargar mas 3 veces
    try:
        # le doy click
        boton.click()
        # espero que cargue la informacion dinamica
        sleep(random.uniform(8.0, 10.0))
        # busco el boton nuevamente para darle click en la siguiente iteracion
        boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
    except:
        # si hay algun error, rompo el lazo. No me complico.
        break

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
autos = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')

# Recorro cada uno de los anuncios que he encontrado
for auto in autos:
    try:
        # Por cada anuncio hallo el precio
        precio = auto.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
        print(precio)
        # Por cada anuncio hallo la descripcion
        descripcion = auto.find_element(By.XPATH, './/div[@data-aut-id="itemTitle"]').text
        print(descripcion)
    except Exception as e:
        print('Anuncio carece de precio o descripcion')
