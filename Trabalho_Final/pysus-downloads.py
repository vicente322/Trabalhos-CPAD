import os
import time
import pandas as pd
from pysus.online_data import SINAN as SINAN_Online
from pysus.online_data import SINASC as SINASC_Online
from pysus.online_data import SIM as SIM_ONLINE
from pysus.ftp.databases.sinan import SINAN
from pysus.ftp.databases.sinasc import SINASC
from pysus.ftp.databases.sim import SIM

init_time = time.time()
states = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', \
          'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', \
          'RR', 'SC', 'SP', 'SE', 'TO']
years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
global sinan, sinasc, sim, sinan_files, sinasc_files, sim_files, parquet_path, csv_path, files_downloaded

def load_databases():
      global sinan, sinasc, sim, sinan_files, sinasc_files, sim_files

      sinan = SINAN().load()
      sinasc = SINASC().load()
      sim = SIM().load()
      sinan_files = sinan.get_files(dis_code=['DENG'], year=years)
      sinasc_files = sinasc.get_files(group='DN', uf=states, year=years)
      sim_files = sim.get_files('CID10', uf=states, year=years)

def check_dir():
      global parquet_path, csv_path

      this_path = os.path.dirname(os.path.abspath(__file__))
      data_bin_name = 'Data'
      data_path = this_path + '/' + data_bin_name + '/'
      parquet_path = data_path + 'Parquet/'
      csv_path = data_path + 'CSV/'

      if not data_bin_name in os.listdir(this_path):
            os.mkdir(data_path)

      if not 'Parquet' in os.listdir(data_path) :
            os.mkdir(parquet_path)

      if not 'CSV' in os.listdir(data_path) :
            os.mkdir(csv_path)

def execute_downloads():
      global files_downloaded
      files_downloaded = 0

      for file in sinan_files:
            if not file.basename.replace('.dbc', '.parquet') in os.listdir(parquet_path) and not file.basename.replace('.dbc', '.csv') in os.listdir(csv_path):
                  print(os.system('clear'))
                  print(f"Arquivos baixados: {files_downloaded}")
                  print(sinan.describe(file))
                  sinan.download(file, local_dir=parquet_path)
                  files_downloaded = files_downloaded + 1
      
      for file in sinasc_files:
            if not file.basename.replace('.dbc', '.parquet') in os.listdir(parquet_path) and not file.basename.replace('.dbc', '.csv') in os.listdir(csv_path):
                  print(os.system('clear'))
                  print(f"Arquivos baixados: {files_downloaded}")
                  print(sinasc.describe(file))
                  sinasc.download(file, local_dir=parquet_path)
                  files_downloaded = files_downloaded + 1

      for file in sim_files:
            if not file.basename.replace('.dbc', '.parquet') in os.listdir(parquet_path) and not file.basename.replace('.dbc', '.csv') in os.listdir(csv_path):
                  print(os.system('clear'))
                  print(f"Arquivos baixados: {files_downloaded}")
                  print(sim.describe(file))
                  sim.download(file, local_dir=parquet_path)
                  files_downloaded = files_downloaded + 1

def transform_data():

      return 

def get_time():
      end_time = time.time()
      run_time = end_time - init_time
      print(f"Tempo total de execução: {run_time:.2f} segundos")
      print(f"Arquivos baixados: {files_downloaded}")


def init():

      load_databases()
      check_dir()
      execute_downloads()
      get_time()

init()