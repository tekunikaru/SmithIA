import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from ferramentas import log

load_dotenv()
ingestor_log = log('IngestorDeDados')


def criar_conexao():
    url = f"mysql+pymysql://{os.getenv('DB_USER', 'xxxx')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'xxxxxxx')}:{os.getenv('DB_PORT', 'xxxx')}/{os.getenv('DB_NAME', 'project_smith')}"
    return create_engine(url)


def processar_arquivo(arquivo, id_maquina, tipo_maquina, sensores):
    if not os.path.exists(arquivo):
        return
    
    df = pd.read_csv(arquivo)
    registros = []
    
    for coluna, sensor in sensores.items():
        if coluna in df.columns:
            registros.append(pd.DataFrame({
                'id_maquina': id_maquina,
                'tipo_maquina': tipo_maquina,
                'timestamp': df['timestamp'],
                'nome_sensor': sensor,
                'valor_sensor': df[coluna]
            }))
    
    if registros:
        pd.concat(registros).to_sql('dados_sensor', criar_conexao(), if_exists='append', index=False)
        ingestor_log.info(f"Processado: {arquivo}")


def ingerir_todos_dados():
    configs = [
        ('caf_98_industrial_data.csv', 'CAF-98-001', 'Moedor Industrial',
         {'consumo_kw': 'consumo_kw', 'temperatura_c': 'temperatura_c', 'vibracao_mm_s': 'vibracao_mm_s'}),
        ('caf_22_balcao_data.csv', 'CAF-22-001', 'Moedor Balcão',
         {'consumo_kw': 'consumo_kw', 'temperatura_c': 'temperatura_c'}),
        ('router_data.csv', 'ROUTER-001', 'Router CNC',
         {'potencia_data': 'potencia_kw', 'spindle_entrada_data': 'spindle_entrada_hz', 'spindle_saida_data': 'spindle_saida_hz'}),
        ('romoes40_data.csv', 'ROMO-ES40-001', 'Torno Romo ES-40',
         {'potencia_kw': 'potencia_kw', 'spindle_carga_kw': 'spindle_carga_kw', 'velocidade_rpm': 'velocidade_rpm'})
    ]
    
    for arquivo, id_maq, tipo, sensores in configs:
        processar_arquivo(arquivo, id_maq, tipo, sensores)


if __name__ == "__main__":
    ingerir_todos_dados()