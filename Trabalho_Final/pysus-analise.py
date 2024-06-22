import os
import pandas as pd

this_path = os.path.dirname(os.path.abspath(__file__))
csv_path = this_path + '/Data/CSV/DENGBR22.csv'

csv = pd.read_csv(csv_path)

print(csv.columns)