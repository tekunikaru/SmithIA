import numpy as np
import pandas as pd
from datetime import datetime

# --- MOEDORES DE CARNE (CONTEXTO CORRIGIDO) ---

def simular_moedor_caf_98():
    """
    Simula um Moedor de Carne Industrial (ex: CAF-98).
    Motor: 2.2 kW (3 CV).
    Sensores: Consumo (kW), Temperatura (°C), Vibração (mm/s).
    """
    print("Gerando dados para: Moedor Industrial CAF-98")
    rng = np.random.default_rng()
    
    # Especificações do Motor e Consumo
    # Motor nominal de 2.2 kW. O consumo médio será um pouco maior (sob carga).
    media_consumo_kw = 2.4  # Consumo médio durante a moagem
    desvio_consumo_kw = 0.5 # Picos ao moer carne mais dura ou com ossos
    
    # Especificações de Temperatura (Motor e Conjunto de Corte)
    media_temp_c = 65.0       # Temperatura de operação normal
    desvio_temp_c = 3.0       # Variação normal
    
    # Especificações de Vibração
    media_vibracao_mm_s = 4.0 # Vibração normal (mm/s RMS)
    desvio_vibracao_mm_s = 0.8  # Variação normal
    
    # Geração de dados
    size = 10_000
    dados_consumo = rng.normal(loc=media_consumo_kw, scale=desvio_consumo_kw, size=size)
    dados_temp = rng.normal(loc=media_temp_c, scale=desvio_temp_c, size=size)
    dados_vibracao = rng.normal(loc=media_vibracao_mm_s, scale=desvio_vibracao_mm_s, size=size)
    
    # Garante que consumo não seja negativo
    dados_consumo = np.abs(dados_consumo) 
    
    # --- Salvar em CSV ---
    horario_geracao = datetime.now()
    data = {
        'consumo_kw': dados_consumo,
        'temperatura_c': dados_temp,
        'vibracao_mm_s': dados_vibracao,
        'timestamp': [horario_geracao] * size
    }
    df = pd.DataFrame(data)
    df.to_csv('caf_98_industrial_data.csv', index=False)
    print("Dados do CAF-98 salvos.")

def simular_moedor_caf_22():
    """
    Simula um Moedor de Carne de Balcão (ex: CAF-22).
    Motor: 0.55 kW (0.75 CV).
    Sensores: Consumo (kW), Temperatura (°C).
    """
    print("Gerando dados para: Moedor de Balcão CAF-22")
    rng = np.random.default_rng()
    
    # Especificações do Motor e Consumo
    # Motor nominal de 0.55 kW.
    media_consumo_kw = 0.6  # Consumo médio durante a moagem
    desvio_consumo_kw = 0.2 # Picos de carga
    
    # Especificações de Temperatura (Motor)
    media_temp_c = 58.0       # Temperatura de operação normal
    desvio_temp_c = 2.5       # Variação normal
    
    # Geração de dados
    size = 10_000
    dados_consumo = rng.normal(loc=media_consumo_kw, scale=desvio_consumo_kw, size=size)
    dados_temp = rng.normal(loc=media_temp_c, scale=desvio_temp_c, size=size)
    
    # Garante que consumo não seja negativo
    dados_consumo = np.abs(dados_consumo)
    
    # --- Salvar em CSV ---
    horario_geracao = datetime.now()
    data = {
        'consumo_kw': dados_consumo,
        'temperatura_c': dados_temp,
        'timestamp': [horario_geracao] * size
    }
    df = pd.DataFrame(data)
    df.to_csv('caf_22_balcao_data.csv', index=False)
    print("Dados do CAF-22 salvos.")


# --- MÁQUINAS CNC (Mantidas do script original) ---

def router():
    print('Gerando dados para: Router CNC')
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
    size = 10_000
    dados_potencia_simulados = rng.normal(loc=media_router_consumo, scale=desvio_router_consumo, size=size)
    dados_spindle_entrada_simulados = rng.normal(loc=media_router_spindle_entrada, scale=desvio_router_spindle_entrada, size=size)   
    dados_spindle_saida_simulados = rng.normal(loc=media_router_spindle_saida, scale=desvio_router_spindle_saida, size=size)

    #---SAVE TO CSV---
    horario_geracao = datetime.now()
    data = {
        'potencia_data': dados_potencia_simulados,
        'spindle_entrada_data': dados_spindle_entrada_simulados,
        'spindle_saida_data': dados_spindle_saida_simulados,
        'timestamp': [horario_geracao] * size
    }
    df = pd.DataFrame(data)
    df.to_csv('router_data.csv', index=False)
    print("Dados do Router CNC salvos.")

def romoes40():
    print('Gerando dados para: Torno Romo ES-40')
    rng = np.random.default_rng()    
    
    #---DADOS DE FAIXA DE VELOCIDADE (Consumo)---
    array_es40_faixa_velocidade = np.array([32, 2360]) # RPM
    
    #---DADOS DO MOTOR PRINCIPAL---
    array_es40_motor_principal = np.array([15, 15, 15, 14]) # kW
    media_es40_motor_principal = np.mean(array_es40_motor_principal)
    desvio_es40_motor_principal = np.std(array_es40_motor_principal)
    
    #---GERAÇÃO DE DADOS SIMULADOS---
    size = 10_000
    
    # Potência simulada (kW)
    dados_potencia_simulados = np.abs(rng.normal(loc=media_es40_motor_principal, scale=desvio_es40_motor_principal, size=size))
    
    # Carga do Spindle (simulada)
    dados_spindle_carga_simulados = np.abs(
        rng.normal(loc=media_es40_motor_principal, scale=desvio_es40_motor_principal, size=size)
    )

    # Velocidade (RPM)
    dados_velocidade_simulados = rng.integers(
        low=array_es40_faixa_velocidade[0],
        high=array_es40_faixa_velocidade[1],
        size=size
    )

    #---SAVE TO CSV---
    horario_geracao = datetime.now()
    data = {
        'potencia_kw': dados_potencia_simulados,
        'spindle_carga_kw': dados_spindle_carga_simulados,
        'velocidade_rpm': dados_velocidade_simulados,
        'timestamp': [horario_geracao] * size
    }
    df = pd.DataFrame(data)
    df.to_csv('romoes40_data.csv', index=False)
    print("Dados do Romo ES-40 salvos.")

# --- Execução ---
if __name__ == "__main__":
    simular_moedor_caf_98()
    simular_moedor_caf_22()
    router()
    romoes40()
    print("\nSimulação de dados concluída.")