from urllib.request import urlopen
import requests
import time
from bs4 import BeautifulSoup

def pega_autores(item):
    url = "https://www.imdb.com"+ item["link"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }


    try:
        response_serie = requests.get(url, headers=headers)
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
        generos = lista_div.find_all('span', class_="ipc-chip__text")
        item["generos"] = [genero.get_text(strip = True) for genero in generos]
        atores = soup.find_all('a', class_="sc-bfec09a1-1 gCQkeh")
        item["atores"] = [ator.get_text(strip=True) for ator in atores]
        poptext = soup.find('div', class_='sc-5f7fb5b4-1 fTREEx')
        if poptext is not None:
            popularidade = poptext.text
            item["popularidade"] = popularidade
        return item
        

import requests
import json
from bs4 import BeautifulSoup
import re   
def dados_series():
    url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"
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
            series = lista_series.find_all('li')#[:10]
        top_series = []
        i = 0
        for serie in series:
            item = {}
            item["titulo"] = serie.find(class_= "ipc-title__text").text.split(" ", 1)[1]
            div = soup.find('div', class_="sc-b0691f29-7 hrgukm cli-title-metadata")
            spans = div.find_all('span', class_="sc-b0691f29-8 ilsLEX cli-title-metadata-item")
            item["ano"] = int(spans[0].text[0:4])
            item["episodios"] = int(spans[1].text.split()[0])
            item["rating"] = float(serie.find(class_= "ipc-rating-star").text[0:3])
            item["link"]= serie.find("a", class_= "ipc-title-link-wrapper")["href"]
            pega_autores(item)
            top_series.append(item)
            i += 1
            print(i)
            if i == 50 or i == 100 or i == 150 or i == 200:
                time.sleep(5)
        with open("series.json", "w") as writeJSON:
            json.dump(top_series, writeJSON, ensure_ascii=False, indent=2)
            
        
dados_series()

        




    
    



            