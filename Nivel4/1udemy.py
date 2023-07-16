import requests
import pandas as pd

headers = {
    # El encabezado de referer es importante. Sin esto, este API en especifico me respondera 403
    "Referer": "https://www.udemy.com/courses/search/?p=2&q=python&src=ukw",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

# Este lazo for me ayudara a iterar el parametro "page" del API
cursos_totales = []
for i in range(1, 2):
    # Esta URL, y los parametros la deciframos gracias al panel de Networks y a una tarea de investigacion
    url_api = 'https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true&p=' + str(i)

    response = requests.get(url_api, headers=headers)
    print(response)
    # Parseo la respuesta en formato JSON. Requests automaticamente lo convierte en un diccionario de Python
    data = response.json()
    print(data)
    # Extraigo los datos del diccionario
    cursos = data["courses"]
    for curso in cursos:
        cursos_totales.append({
            "title": curso["title"],
            "num_reviews": curso["num_reviews"],
            "rating": curso["rating"]
        })
        # print (curso["title"])
        # print (curso["num_reviews"])
        # print (curso["rating"])

    # Hago que el usuario tenga que aplastar enter antes de seguir a la siguiente pagina
    input()

df = pd.DataFrame(cursos_totales)

print(df)

df.to_csv("cursos_udemy.csv")
