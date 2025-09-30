import pandas as pd

data = pd.read_csv('registros_maquinas.csv')

print(data.loc[data['id_maquina'] == 4] )