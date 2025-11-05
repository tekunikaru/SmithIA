import pandas as pd
from ferramentas import execute_query, log
import os

ingestor_log = log('IngestorDeDados')

def ingerir_csv_para_db(caminho_arquivo: str, id_maquina: str, tipo_maquina: str, mapeamento_sensores: dict):
    """
    Lê um arquivo CSV e ingere seus dados na tabela sensor_data.
    :param caminho_arquivo: Caminho para o arquivo CSV.
    :param id_maquina: Identificador da máquina.
    :param tipo_maquina: Tipo da máquina.
    :param mapeamento_sensores: Dicionário mapeando nomes das colunas CSV para sensor_name no BD.
    """
    if not os.path.exists(caminho_arquivo):
        ingestor_log.warning(f"Arquivo CSV não encontrado: {caminho_arquivo}. Pulando ingestão.")
        return

    df = pd.read_csv(caminho_arquivo)
    registros_para_inserir = []

    for indice, linha in df.iterrows():
        timestamp = linha['timestamp']
        for coluna_csv, nome_sensor_bd in mapeamento_sensores.items():
            if coluna_csv in linha:
                registros_para_inserir.append((
                    id_maquina,
                    tipo_maquina,
                    timestamp,
                    nome_sensor_bd,
                    linha[coluna_csv]
                ))

    if registros_para_inserir:
        # Usando executemany para eficiência
        query = """
            INSERT INTO sensor_data (machine_id, machine_type, timestamp, sensor_name, sensor_value)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            conn = None
            cursor = None
            conn = execute_query(query, tuple(registros_para_inserir[0]), fetchone=False, fetchall=False) # Apenas para obter uma conexão
            # Este é um workaround pois execute_query não suporta executemany diretamente.
            # Para uma aplicação real, execute_query deveria ser refatorado para suportar executemany.
            # Por enquanto, vou abrir uma conexão direta para executemany.
            import mariadb
            from dotenv import load_dotenv
            load_dotenv()
            conn = mariadb.connect(
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                host=os.getenv("DB_HOST", "127.0.0.1"),
                port=int(os.getenv("DB_PORT", 3306)),
                database=os.getenv("DB_NAME", "project_smith")
            )
            cursor = conn.cursor()
            cursor.executemany(query, registros_para_inserir)
            conn.commit()
            ingestor_log.info(f"Ingeridos com sucesso {len(registros_para_inserir)} registros de {caminho_arquivo} para sensor_data.")
        except mariadb.Error as e:
            ingestor_log.error(f"Erro ao ingerir dados de {caminho_arquivo}: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        ingestor_log.info(f"Nenhum registro para ingerir de {caminho_arquivo}.")


def ingerir_todos_dados():
    ingestor_log.info("Iniciando ingestão de dados...")

    # CAF-98 Industrial
    ingerir_csv_para_db(
        'caf_98_industrial_data.csv',
        'CAF-98-001',
        'Moedor Industrial',
        {
            'consumo_kw': 'consumo_kw',
            'temperatura_c': 'temperatura_c',
            'vibracao_mm_s': 'vibracao_mm_s'
        }
    )

    # CAF-22 Balcão
    ingerir_csv_para_db(
        'caf_22_balcao_data.csv',
        'CAF-22-001',
        'Moedor Balcão',
        {
            'consumo_kw': 'consumo_kw',
            'temperatura_c': 'temperatura_c'
        }
    )

    # Router CNC
    ingerir_csv_para_db(
        'router_data.csv',
        'ROUTER-001',
        'Router CNC',
        {
            'potencia_data': 'potencia_kw',
            'spindle_entrada_data': 'spindle_entrada_hz',
            'spindle_saida_data': 'spindle_saida_hz'
        }
    )

    # Romo ES-40
    ingerir_csv_para_db(
        'romoes40_data.csv',
        'ROMO-ES40-001',
        'Torno Romo ES-40',
        {
            'potencia_kw': 'potencia_kw',
            'spindle_carga_kw': 'spindle_carga_kw',
            'velocidade_rpm': 'velocidade_rpm'
        }
    )
    ingestor_log.info("Ingestão de dados concluída.")

if __name__ == "__main__":
    # Garantir que as tabelas existam antes de ingerir dados
    from db_schema import create_tables
    create_tables()
    ingerir_todos_dados()
