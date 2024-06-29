import pandas as pd
import os

# Lista de estados que queremos, índices de acordo com tabela do IBGE: https://www.ibge.gov.br/explica/codigos-dos-municipios.php
# GO=52
# SP=35
# ES=32
# RS=43
sg_uf_list = [32, 35, 43, 52]

def filter_data_by_ufs(file_name):
    output_dir = './Data/Filtered_CSV'
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv("./Data/CSV/" + file_name, sep=';', low_memory=False)
    
    df['SG_UF'] = pd.to_numeric(df['SG_UF'].str.strip(), errors='coerce')
    # Drop rows with NaN values in SG_UF
    df = df.dropna(subset=['SG_UF'])
    # Convert SG_UF to integers
    df['SG_UF'] = df['SG_UF'].astype(int)
    # Filter the DataFrame
    df_filtered = df[df['SG_UF'].isin(sg_uf_list)]

    df_filtered.to_csv("./Data/Filtered_CSV/" + file_name, index=False, sep=';')
    print("Filtered data saved back to", "./Data/Filtered_CSV/" + file_name)

filter_data_by_ufs("DENGBR13.csv")
filter_data_by_ufs("DENGBR14.csv")
filter_data_by_ufs("DENGBR15.csv")
filter_data_by_ufs("DENGBR16.csv")
filter_data_by_ufs("DENGBR17.csv")
filter_data_by_ufs("DENGBR18.csv")
filter_data_by_ufs("DENGBR19.csv")
filter_data_by_ufs("DENGBR20.csv")
filter_data_by_ufs("DENGBR21.csv")
filter_data_by_ufs("DENGBR22.csv")