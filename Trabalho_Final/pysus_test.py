import pandas as pd
from pysus.online_data import IBGE
import ipywidgets as widgets
import os

ag = IBGE.list_agregados()
opts= [(r.nome, int(r.id)) for r in pd.DataFrame(ag[ag.id=='CM'].agregados.iloc[0]).itertuples()]
ds = IBGE.FetchData(475,periodos=1996,variavel=93,localidades='N3[all]',
                              classificacao='58[all]|2[4,5]|1[all]',view='flat')

pandas_ds = ds.to_dataframe()

pandas_ds.to_csv(path_or_buf = (os.getcwd() + '/Trabalho_Final/Data/pysus_data.csv'), index = False)