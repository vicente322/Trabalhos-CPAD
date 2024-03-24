from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
import time

link_list = []
html_list = []

def busca_links(site):
      soup = BeautifulSoup(site.read(), 'html.parser')
      table=soup.find_all('td')
      
      for tag in table:
            tag_link = tag.next_element.next_element
            link_list.append(tag_link.attrs['href'])

      for tag in soup.find_all('a'):
            if tag.string == "Next >":
                  if 'href' in tag.attrs:
                        html = urlopen('http://127.0.0.1:8000' + tag.attrs['href'])
                        busca_links(html)

def baixa_pagina():
      for link in link_list:
            linksoup = urlopen('http://127.0.0.1:8000' + link)
            html = BeautifulSoup(linksoup.read(), 'html.parser')
            sigla = ''
            for tag in html.find_all('td', class_="w2p_fw"):
                  if tag.previous_element == "Iso: ":
                        sigla = tag.string
            dic = {"sigla": sigla, "html":html}
            html_list.append(dic)

def salva_dados():
      with open ('paises.csv', 'w', newline='') as csvfile:
            escritor = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            escritor.writerow(['Pais','Capital', 'Area', 'Paises vizinhos'])

            for html in html_list:

                  nome = ''
                  capital = ''
                  area = 0
                  vizinhos = ''
                  timestamp = 0

                  for tag in html.get("html").find_all('td', class_="w2p_fw"):
                        if tag.previous_element == "Country: ":
                              nome = tag.string
                        
                        if tag.previous_element == "Capital: ":
                              capital = tag.string
                        
                        if tag.previous_element == "Area: ":
                              area = tag.string.replace(' square kilometres', '')

                        if tag.previous_element == "Neighbours: ":
                              for link in tag.find_all('a'):
                                    if link['href'] != '/places/default/iso//':
                                          sigla = link['href'].replace('/places/default/iso/', '')
                                          for pais in html_list:
                                                if pais.get("sigla") == sigla:
                                                      for tagVizinho in pais.get("html").find_all('td', class_="w2p_fw"):
                                                            if tagVizinho.previous_element == "Country: ":
                                                                  if vizinhos != '':
                                                                        vizinhos += ', '
                                                                  vizinhos += tagVizinho.string
                                                                  
                        timestamp = time.time()

                  escritor.writerow([nome, capital, area, vizinhos, timestamp])

def confere_lista():
      i = 0
      dados = []
      erros = False

      with open ('paises.csv', newline='') as csvfile:
            leitor = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in leitor:
                  if i == 0:
                        dados.append(row)
                  else:
                        paisCSV = row[0]
                        capitalCSV = row[1]
                        areaCSV = row[2]
                        paisesVizCSV = row[3]

                        paisHTML = ''
                        capitalHTML = ''
                        areaHTML = ''
                        paisesVizHTML = ''

                        html = html_list[i-1]

                        for tag in html.get("html").find_all('td', class_="w2p_fw"):
                              if tag.previous_element == "Country: ":
                                    paisHTML = tag.string
                              if tag.previous_element == "Capital: ":
                                    capitalHTML = tag.string
                                    if capitalHTML is None:
                                          capitalHTML = ''
                              if tag.previous_element == "Area: ":
                                    areaHTML = tag.string.replace(' square kilometres', '')
                              if tag.previous_element == "Neighbours: ":
                                    for link in tag.find_all('a'):
                                          if link['href'] != '/places/default/iso//':
                                                sigla = link['href'].replace('/places/default/iso/', '')
                                                for pais in html_list:
                                                      if pais.get("sigla") == sigla:
                                                            for tagVizinho in pais.get("html").find_all('td', class_="w2p_fw"):
                                                                  if tagVizinho.previous_element == "Country: ":
                                                                        if paisesVizHTML != '':
                                                                              paisesVizHTML += ', '
                                                                        paisesVizHTML += tagVizinho.string

                        if paisCSV != paisHTML or capitalCSV != capitalHTML or areaCSV != areaHTML or paisesVizCSV != paisesVizHTML:
                              timestamp = time.time()
                              dados.append([paisHTML, capitalHTML, areaHTML, paisesVizHTML, timestamp])
                              erros = True
                        else:
                              dados.append(row)

                        if paisCSV != paisHTML:
                              print(paisCSV)
                              print('nomes diferentes\n')
                        if capitalCSV != capitalHTML:
                              print(paisCSV)
                              print('capital diferente')
                              print('html')
                              print(capitalHTML.__class__)
                              print('csv')
                              print(capitalCSV.__class__)
                        if areaCSV != areaHTML:
                              print(paisCSV)
                              print('area diferente')
                              print('area html: |' + str(areaHTML) + '|')
                              print('area csv: |' + str(areaCSV) + '|\n')
                        if paisesVizCSV != paisesVizHTML:
                              print(paisCSV)
                              print('vizinhos diferentes\n')
                        
                  i += 1
      

      

      if erros:
            print('erro')
            with open ('paises.csv', 'w', newline='') as csvfile:
                  escritor = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                  for linha in dados:
                        escritor.writerow(linha)

def monitora():
      while 1 == 1:
            time.sleep(15)
            html_list=[]
            baixa_pagina()
            confere_lista()
            print('loop')
            


            
html = urlopen('http://127.0.0.1:8000/places/default/index')

busca_links(html)

baixa_pagina()

salva_dados()

monitora()