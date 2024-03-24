import csv

lista = [1,2,3,4]

def confere_lista():
      with open ('paises.csv', newline='') as csvfile:
            leitor = csv.reader(csvfile, delimiter=';', quotechar='|')
            i = 0
            for row in leitor:
                  if i != 0:
                        string = ', '.join(row)
                        print(row)
                                                
                  i += 1
            
# confere_lista()
                  

