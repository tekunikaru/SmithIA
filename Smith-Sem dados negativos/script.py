import numpy as np
import pandas as pd
from datetime import datetime

current_time = datetime.now()

def caf114():
    print('MAQUINA 1')
    rng = np.random.default_rng()
    #---MOTOR-----
    array_caf114_potenciamotor = np.array([7.5,7.3,7.7]) 
    desvio_motor = np.std(array_caf114_potenciamotor)  
    media_motor = np.mean(array_caf114_potenciamotor)
    
    #---POTENCIA---
    array_caf_114_consumo = np.array([8.36, 8.32, 8.38, 8.36, 8.3, 8.29, 7.89, 8.98, 8.33, 8.34, 8.36, 8.39, 8.41, 8.36, 8.35, 8.34])
    desvio_consumo = np.std(array_caf_114_consumo)
    media_consumo = np.mean(array_caf_114_consumo)
    
    #---METODOS MOTOR---
    rng_dados_motor = rng.normal(loc=media_motor, scale=desvio_motor, size=10_000)   
    
    #---METODOS POTENCIA---
    rng_dados_potencia = rng.normal(loc=media_consumo, scale=desvio_consumo, size=10_000)

    #---SAVE TO CSV---
    horario_geracao = current_time
    data = {
        'motor_data': rng_dados_motor,
        'potencia_data': rng_dados_potencia,
        'timestamp': [horario_geracao] * len(rng_dados_motor)
    }
    df = pd.DataFrame(data)
    df.to_csv('caf114_data.csv', index=False)
    
    return rng_dados_motor, rng_dados_potencia, horario_geracao

def cafft030():
    print('MAQUINA 2')
    rng1 = np.random.default_rng()
    #---MOTOR-----
    array_caf_ft030_motor= np.array([0.18,0.20,0.16]) 
    desvio_motor = np.std(array_caf_ft030_motor)  
    media_motor = np.mean(array_caf_ft030_motor)
    
    #---POTENCIA---
    array_caf_ft030_potencia = np.array([0.30,0.24,0.40,0.38,0.27,0.22,0.37,0.43,0.31,0.29,0.45])
    desvio_consumo = np.std(array_caf_ft030_potencia)
    media_consumo = np.mean(array_caf_ft030_potencia)
    
    #---METODOS MOTOR---
    rng_dados_motor = rng1.normal(loc=media_motor, scale=desvio_motor, size=10_000)   
    
    #---METODOS POTENCIA---
    rng_dados_potencia = rng1.normal(loc=media_consumo, scale=desvio_consumo, size=10_000)

    #---SAVE TO CSV---
    horario_geracao = current_time
    data = {
        'motor_data': rng_dados_motor,
        'potencia_data': rng_dados_potencia,
        'timestamp': [horario_geracao] * len(rng_dados_motor)
    }
    df = pd.DataFrame(data)
    df.to_csv('cafft030_data.csv', index=False)

    return rng_dados_motor, rng_dados_potencia, horario_geracao

def router():
    rng = np.random.default_rng()    
    
    #---DADOS DE POTÊNCIA (Consumo)---
    array_router_potencia = np.array([2.2,2.4,2.1,2.22,2.12,2.30,2.35,2.18,2.40,2.32,2.28])
    media_router_consumo = np.mean(array_router_potencia)
    desvio_router_consumo = np.std(array_router_potencia)
    
    #---DADOS DO SPINDLE ENTRADA (Frequência da Rede)---
    array_router_spindle_entrada = np.array([48,63,49,54,53,58])
    media_router_spindle_entrada = np.mean(array_router_spindle_entrada)
    desvio_router_spindle_entrada = np.std(array_router_spindle_entrada)

    #---DADOS DO SPINDLE SAIDA (Frequência da Rede)---    
    array_router_spindle_saida = np.array([400, 400, 400, 399, 400, 398, 400, 401])
    media_router_spindle_saida = np.mean(array_router_spindle_saida)
    desvio_router_spindle_saida = np.std(array_router_spindle_saida)
    
    #---GERAÇÃO DE DADOS SIMULADOS---
    dados_potencia_simulados = rng.normal(loc=media_router_consumo, scale=desvio_router_consumo, size=10_000)
    dados_spindle_entrada_simulados = rng.normal(loc=media_router_spindle_entrada, scale=desvio_router_spindle_entrada, size=10_000)   
    dados_spindle_saida_simulados = rng.normal(loc=media_router_spindle_saida, scale=desvio_router_spindle_saida, size=10_000)

    #---SAVE TO CSV---
    horario_geracao = current_time
    data = {
        'potencia_data': dados_potencia_simulados,
        'spindle_entrada_data': dados_spindle_entrada_simulados,
        'spindle_saida_data': dados_spindle_saida_simulados,
        'timestamp': [horario_geracao] * len(dados_potencia_simulados)
    }
    df = pd.DataFrame(data)
    df.to_csv('router_data.csv', index=False)

    return dados_potencia_simulados, dados_spindle_entrada_simulados, dados_spindle_saida_simulados, horario_geracao

def romoes40():
    rng = np.random.default_rng()    
    
    #---DADOS DE FAIXA DE VELOCIDADE (Consumo)---
    # Representa a faixa de variação da velocidade da máquina (mínimo e máximo)
    array_es40_faixa_velocidade = np.array([32, 2360])
    
    #---DADOS DO MOTOR PRINCIPAL---
    array_es40_motor_principal = np.array([15, 15, 15, 14])
    media_es40_motor_principal = np.mean(array_es40_motor_principal)
    desvio_es40_motor_principal = np.std(array_es40_motor_principal)
    
    #---GERAÇÃO DE DADOS SIMULADOS---
    # Potência simulada sempre positiva (usando valor absoluto)
    dados_potencia_simulados = np.abs(rng.normal(loc=50, scale=10, size=10_000))
    
    # Spindle entrada simulada sempre positiva
    dados_spindle_entrada_simulados = np.abs(
        rng.normal(loc=media_es40_motor_principal, scale=desvio_es40_motor_principal, size=10_000)
    )

    # Velocidade simulada dentro da faixa definida
    dados_velocidade_simulados = rng.integers(
        low=array_es40_faixa_velocidade[0],
        high=array_es40_faixa_velocidade[1],
        size=10_000
    )

    #---SAVE TO CSV---
    horario_geracao = datetime.now().isoformat()
    data = {
        'potencia_data': dados_potencia_simulados,
        'spindle_entrada_data': dados_spindle_entrada_simulados,
        'velocidade_data': dados_velocidade_simulados,
        'timestamp': [horario_geracao] * len(dados_potencia_simulados)
    }
    df = pd.DataFrame(data)
    df.to_csv('romoes40_data.csv', index=False)

    return dados_potencia_simulados, dados_spindle_entrada_simulados, dados_velocidade_simulados, horario_geracao

caf114()
cafft030()
router()
romoes40()