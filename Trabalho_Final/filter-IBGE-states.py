import os
import pandas as pd

data_path = os.path.dirname(os.path.abspath(__file__)) + '/Data/IBGE/'
csv_path = data_path + 'CSV/'
xls_path = data_path + 'XLS/'
file_name = 'complete_censo.csv'

states = ['Goiás', 'São Paulo', 'Espírito Santo', 'Rio Grande do Sul']
new_rows = []

df01_20 = pd.read_excel(io= xls_path + 'serie_2001_2020_TCU.xls')
df01_20 = df01_20.dropna()
for i in range(20):
      for line in df01_20.itertuples():
            if line[1] in states:
                  uf = ''
                  if line[1] == 'Goiás':
                        uf = 'GO'
                  elif line[1] == 'São Paulo':
                        uf = 'SP'
                  elif line[1] == 'Espírito Santo':
                        uf = 'ES'
                  elif line[1] == 'Rio Grande do Sul':
                        uf = 'RS'
                  if (2001 + i) >= 2013:
                        row = {'Ano':2001 + i, 'UF': uf, 'Est_Pop': line[i + 2]}
                        new_rows.append(row)

df2021 = pd.read_excel(io= xls_path + 'estimativa_dou_2021.xls')
df2021 = df2021[df2021['BRASIL E UNIDADES DA FEDERAÇÃO'].isin(states)]
for line in df2021.itertuples():
      uf = ''
      if line[1] == 'Goiás':
            uf = 'GO'
      elif line[1] == 'São Paulo':
            uf = 'SP'
      elif line[1] == 'Espírito Santo':
            uf = 'ES'
      elif line[1] == 'Rio Grande do Sul':
            uf = 'RS'

      row = {'Ano':2021, 'UF': uf, 'Est_Pop': line[3]}
      new_rows.append(row)

df2020 = pd.read_csv(filepath_or_buffer=csv_path + 'censo2022.csv', sep = ';')

for line in df2020.itertuples():
      if line[4] == 'GO' or line[4] == 'SP' or line[4] == 'ES' or line[4] == 'RS':
            row = {'Ano':line[1], 'UF': line[4], 'Est_Pop': line[2]}
            new_rows.append(row)

new_df = pd.DataFrame(new_rows)
new_df.to_csv(path_or_buf=csv_path + file_name, sep = ';', index=False)
print(new_df)