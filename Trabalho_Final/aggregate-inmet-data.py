import os
import pandas as pd
import unicodedata
import re

def normalize_column_name(col_name):
    # Normalize the column name by removing special characters and converting to ASCII
    nfkd_form = unicodedata.normalize('NFKD', col_name)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('ASCII')
    # Replace spaces with underscores and convert to lowercase
    normalized = re.sub(r'\s+', '_', only_ascii).lower()
    # Handle specific case for '(c)' in column names
    normalized = normalized.replace('_(c)', '_c')
    normalized = normalized.replace('_(i12c)', '_c')
    return normalized

def read_and_process_csv(file_path):
    # Read the CSV file, handle special characters by specifying the encoding
    df = pd.read_csv(file_path, encoding='latin1', sep=';', skiprows=8)
    
    # Print the columns to debug after reading
    print(f"Columns in {file_path} after reading: {df.columns}")
    
    # Normalize column names
    df.columns = [normalize_column_name(col) for col in df.columns]
    
    # Print the columns to debug after normalization
    print(f"Columns in {file_path} after normalization: {df.columns}")
    
    # Define the column mappings you are interested in
    column_mappings = {
        'data_(yyyy-mm-dd)': 'Data',
        'data': 'Data',
        'hora_(utc)': 'Hora UTC',
        'precipitacao_total,_horario_(mm)': 'Precipitacao',
        'pressao_atmosferica_ao_nivel_da_estacao,_horaria_(mb)': 'Pressao Estacao',
        'pressao_atmosferica_max.na_hora_ant._(aut)_(mb)': 'Pressao Max',
        'pressao_atmosferica_min._na_hora_ant._(aut)_(mb)': 'Pressao Min',
        'radiacao_global_(kj/m2)': 'Radiacao Global',
        'temperatura_do_ar_-_bulbo_seco,_horaria_c': 'Temp Ar',
        'temperatura_do_ponto_de_orvalho_c': 'Temp Orvalho',
        'temperatura_maxima_na_hora_ant._(aut)_c': 'Temp Max',
        'temperatura_minima_na_hora_ant._(aut)_c': 'Temp Min',
        'temperatura_orvalho_max._na_hora_ant._(aut)_c': 'Temp Orvalho Max',
        'temperatura_orvalho_min._na_hora_ant._(aut)_c': 'Temp Orvalho Min',
        'umidade_rel._max._na_hora_ant._(aut)_(%)': 'Umidade Rel Max',
        'umidade_rel._min._na_hora_ant._(aut)_(%)': 'Umidade Rel Min',
        'umidade_relativa_do_ar,_horaria_(%)': 'Umidade Rel',
        'vento,_direcao_horaria_(gr)_(_(gr))': 'Vento Direcao',
        'vento,_rajada_maxima_(m/s)': 'Vento Rajada Max',
        'vento,_velocidade_horaria_(m/s)': 'Vento Velocidade'
    }
    
    # Rename columns based on the available columns in the CSV
    df.rename(columns=column_mappings, inplace=True)
    
    # Check if 'Temp Ar' and 'Umidade Rel' columns are present
    required_columns = ['Temp Ar', 'Umidade Rel']
    if not set(required_columns).issubset(df.columns):
        missing_columns = list(set(required_columns) - set(df.columns))
        raise KeyError(f"Columns not found: {missing_columns}")
    
    if 'Data' not in df.columns:
        raise KeyError(f"'Data' column not found in {file_path}")
    
    # Try parsing 'Data' column with multiple date formats
    try:
        df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    except ValueError:
        df['Data'] = pd.to_datetime(df['Data'], format='%Y/%m/%d')
    
    # Clean numeric columns of commas
    numeric_columns = ['Temp Ar', 'Umidade Rel']
    
    df[numeric_columns] = df[numeric_columns].replace(',', '', regex=True).astype(float)
    
    return df

def aggregate_data_by_day(df):
    # Group by date and calculate mean of 'Temp Ar' and 'Umidade Rel'
    daily_means = df.groupby(df['Data'].dt.date)[['Temp Ar', 'Umidade Rel']].mean()
    return daily_means

def save_aggregated_data(state, year, aggregated_df):
    output_dir = f'./Data/INMET/dados_agregados/{year}'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{state}_{year}_aggregated.csv')
    aggregated_df.to_csv(output_file, index_label='Data', encoding='utf-8')

def process_yearly_data(year_dir, year):
    for file_name in os.listdir(year_dir):
        if file_name.endswith('.csv') or file_name.endswith('.CSV'):
            state = file_name.split('_')[2]
            file_path = os.path.join(year_dir, file_name)
            
            df = read_and_process_csv(file_path)
            aggregated_df = aggregate_data_by_day(df)
            save_aggregated_data(state, year, aggregated_df)

def main():
    base_dir = './Data/INMET/dados_originais'
    for year in range(2013, 2023):
        year_dir = os.path.join(base_dir, str(year))
        process_yearly_data(year_dir, year)

if __name__ == "__main__":
    main()
