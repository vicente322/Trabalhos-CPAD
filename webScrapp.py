from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

link_list = []

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


html = urlopen('http://127.0.0.1:8000/places/default/index')

busca_links(html)

print(link_list)