from script import maquina_1, maquina_2, maquina_3
import pandas as pd
import datetime
import pickle

rng_m_1, rng_p_1 = maquina_1()
rng_m_2, rng_p_2 = maquina_2()
rng_p_3, rng_spindle_entrada_3, rng_spindle_saida_3 = maquina_3()
hora_atual = datetime.datetime.now()

registros = []

#Maquina 1 e 2
for (vm1, vp1, vm2, vp2) in zip(rng_m_1, rng_p_1, rng_m_2, rng_p_2):
    #Maquina1
    registros.append({'id_maquina': 1, 'variavel': 'motor', 'valor': vm1, 'timestamp': hora_atual.strftime('%Y-%m-%d %H:%M')})
    registros.append({'id_maquina': 1, 'variavel': 'potencia', 'valor': vp1, 'timestamp': hora_atual.strftime('%Y-%m-%d %H:%M')})

    #Maquina2
    registros.append({'id_maquina': 2, 'variavel': 'motor', 'valor': vm2,'timestamp': hora_atual.strftime('%Y-%m-%d %H:%M')})
    registros.append({'id_maquina': 2 , 'variavel': 'potencia', 'valor': vp2, 'timestamp': hora_atual.strftime('%Y-%m-%d %H:%M')})

for (vp3, v_SE, v_SS) in zip(rng_p_3, rng_spindle_entrada_3, rng_spindle_saida_3):
    #maquina3
    registros.append({'id_maquina': 3, 'variavel': 'potencia', 'valor': vp3, 'timestamp': hora_atual.strftime('%Y-%m-%d %H:%M')})
    registros.append({'id_maquina': 3, 'variavel': 'spindle_entrada', 'valor': v_SE, 'timestamp': hora_atual.strftime('%Y-%m-%d %H:%M')})
    registros.append({'id_maquina': 3, 'variavel': 'spindle_saida', 'valor': v_SS, 'timestamp': hora_atual.strftime('%Y-%m-%d %H:%M')})

df = pd.DataFrame(registros)
df["timestamp"] = pd.to_datetime(df["timestamp"])

with open('dataframe_smith.pickle', 'wb') as f:
    pickle.dump(df, f)

print(df[df['id_maquina'] == 3])