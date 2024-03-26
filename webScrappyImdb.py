from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

def pega_autores(link):
    url = "https://www.imdb.com"+link
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }


    try:
        response_serie = requests.get(url, headers=headers)  # Corrigindo a passagem da URL
        response_serie.raise_for_status()
    except requests.HTTPError as e:
        print("The server returned an HTTP error:", e)
        return None
    except requests.RequestException as e:
        print("Request error:", e)
        return None
    else:
        html_serie = response_serie.text
        soup = BeautifulSoup(html_serie, 'html.parser')
        lista_div = soup.find('div', class_="ipc-chip-list__scroller")
        lista_span = lista_div.find_all('span', class_="ipc-chip__text")
        print("Generos: ")
        for span in lista_span:
            print(span.text)
        list_atores = soup.find_all('a', class_="sc-bfec09a1-1 gCQkeh")
        print("Atores: ")
        for ator in list_atores:
           print(ator.text)
        popularidade = soup.find('div', class_='sc-5f7fb5b4-1 fTREEx')
        print("Popularidade:", popularidade.text)

import requests
from bs4 import BeautifulSoup
import re   

url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"

# Adicionando um cabeçalho de usuário
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.HTTPError as e:
    print("The server returned an HTTP error:", e)
except requests.RequestException as e:
    print("Request error:", e)
else:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    lista_series = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI compact-list-view ipc-metadata-list--base")
    if lista_series:
        series = lista_series.find_all('li')
        
    for serie in series:
        titulo_elemento = serie.find(class_= "ipc-title__text").text
        print(titulo_elemento)
        ano_estreia_elemento = serie.find(class_="sc-b0691f29-8 ilsLEX cli-title-metadata-item").text
        div = soup.find('div', class_="sc-b0691f29-7 hrgukm cli-title-metadata")
        spans = div.find_all('span', class_="sc-b0691f29-8 ilsLEX cli-title-metadata-item")
        
        if len(spans)>= 2:
            numero_episodios = spans[1].text
            print(numero_episodios)
            
        rating = serie.find(class_= "ipc-rating-star").text
        link_pagina_filme = serie.find("a", class_= "ipc-title-link-wrapper")
        re2_result = re.search(r'\d{4}',ano_estreia_elemento)
        
        if re2_result:
            ano_estreia_elemento = re.search(r'\d{4}',ano_estreia_elemento).group(0)
            print(ano_estreia_elemento)
            
        re_result = re.search(r'^\d\.\d',rating) #aplicando a regex para extrair apenas o padrão 'digito ponto digito'
        
        if re_result:
            rating = re.search(r'^\d\.\d',rating).group(0) #string resultante da regex
            print(rating)
            
        link = link_pagina_filme["href"]
        print(link)
        pega_autores(link)





    



            