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

def baixa_pagina(link):
      linksoup = urlopen('http://127.0.0.1:8000' + link)
      html = BeautifulSoup(linksoup.read(), 'html.parser')
      sigla = ''
      for tag in html.find_all('td', class_="w2p_fw"):
            if tag.previous_element == "Iso: ":
                  sigla = tag.string
      dic = {"sigla": sigla, "html":html}
      html_list.append(dic)
      # html_list.append(BeautifulSoup(linksoup.read(), 'html.parser'))

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
                              area = int(tag.string.replace(' square kilometres', ''))

                        if tag.previous_element == "Neighbours: ":
                              for link in tag.find_all('a'):
                                    if link['href'] != '/places/default/iso//':
                                          sigla = link['href'].replace('/places/default/iso/', '')
                                          # print(sigla)
                                          for pais in html_list:
                                                # print(pais.get("sigla"))
                                                if pais.get("sigla") == sigla:
                                                      for tagVizinho in pais.get("html").find_all('td', class_="w2p_fw"):
                                                            if tagVizinho.previous_element == "Country: ":
                                                                  if vizinhos != '':
                                                                        vizinhos += ', '
                                                                  vizinhos += tagVizinho.string
                                                                  
                        timestamp = time.time()

                  escritor.writerow([nome, capital, area, vizinhos, timestamp])

            
html = urlopen('http://127.0.0.1:8000/places/default/index')

busca_links(html)
for link in link_list:
      baixa_pagina(link)

salva_dados()
