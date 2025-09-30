from script import caf114, cafft030, router, romoes40
import csv
import datetime

rng_m_1, rng_p_1 = caf114()
rng_m_2, rng_p_2 = cafft030()
rng_p_3, rng_spindle_entrada_3, rng_spindle_saida_3 = router()
rng_p_4, rng_spindle_entrada_4 = romoes40()

hora_atual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

registros = []

# Maquina 1 e 2
for (vm1, vp1, vm2, vp2) in zip(rng_m_1, rng_p_1, rng_m_2, rng_p_2):
    registros.append([1, 'motor', vm1, hora_atual])
    registros.append([1, 'potencia', vp1, hora_atual])
    registros.append([2, 'motor', vm2, hora_atual])
    registros.append([2, 'potencia', vp2, hora_atual])

# Maquina 3
for (vp3, v_SE, v_SS) in zip(rng_p_3, rng_spindle_entrada_3, rng_spindle_saida_3):
    registros.append([3, 'potencia', vp3, hora_atual])
    registros.append([3, 'spindle_entrada', v_SE, hora_atual])
    registros.append([3, 'spindle_saida', v_SS, hora_atual])

for (vp4, v_SE) in zip(rng_p_4, rng_spindle_entrada_4):
    registros.append([4, 'potencia', vp4, hora_atual])
    registros.append([4, 'spindle_entrada', v_SE, hora_atual])

# Ecrevendo diretamente no CSV
with open('registros_maquinas.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id_maquina', 'variavel', 'valor', 'timestamp']) #cabeçalho
    writer.writerows(registros)