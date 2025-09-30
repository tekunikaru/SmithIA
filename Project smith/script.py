import numpy as np

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
    
    return rng_dados_motor, rng_dados_potencia

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

    return rng_dados_motor, rng_dados_potencia

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

    return dados_potencia_simulados, dados_spindle_entrada_simulados, dados_spindle_saida_simulados

def romoes40():
    rng = np.random.default_rng()    
    
    #---DADOS DE FAIXA DE VELOCIDADE (Consumo)---
    array_es40_faixa_velocidade = np.array([32, 2360])
    
    #---DADOS DO MOTOR PRINCIPAL---
    array_es40_motor_principal = np.array([15,15,15,14])
    media_es40_motor_principal = np.mean(array_es40_motor_principal)
    desvio_es40_motor_principal = np.std(array_es40_motor_principal)
    
    #---GERAÇÃO DE DADOS SIMULADOS---
    dados_potencia_simulados = rng.normal(size=10_000)
    dados_spindle_entrada_simulados = rng.normal(loc=media_es40_motor_principal, scale=desvio_es40_motor_principal, size=10_000)


    return dados_potencia_simulados, dados_spindle_entrada_simulados
