import mariadb
from config_log import log
from regras_sensores import sensores
import json
import datetime

def database(consulta: str) -> list:
    conn = mariadb.connect(
        user="xxxx",
        host="xxxxxx",
        port='xxxx',
        database="project_smith"
    )
    cur = conn.cursor()
    cur.execute(consulta)
    resultados = cur.fetchall()
    return resultados

def execute_query(consulta: str) -> str:
    """
    Executa comandos SQL no banco de dados SQL Server local.
    
    Retorna:
      - Para SELECT: Uma lista de dicionários (chave=nome da coluna, valor=dado).
      - Para DML (INSERT/UPDATE/DELETE): Uma lista com um dicionário contendo as linhas afetadas.
    """
    print(consulta)
    try:
        conn = mariadb.connect(
            user="xxxx",
            host="xxxxx",
            port='xxxx',
            database="project_smith" )
        cur = conn.cursor()
        cur.execute(consulta)

        if consulta.strip().upper().startswith(('SELECT', 'WITH')):
            columns = [column[0] for column in cur.description]
            rows = cur.fetchall()
            resultados = [dict(zip(columns, row)) for row in rows]

            return str(resultados)
        
        else:
            conn.commit()
            return [{"linhas_afetadas": cur.rowcount}]

    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return [{"erro": str(e)}]

    
def verificar_sensor(id_maquina: str, nome_sensor: str, valor_sensor: float) -> dict:
    '''
    Verifica o sensor da maquina que foi passado como argumento
    Args:
        id_maquina: nome da maquina a ser verficada
        nome_sensor: tipo do sensor 
        valor_sensor: valor lido do sensor
    
    Returns:
        json: status e menssagem 

    '''
    sensor_maquina = sensores[id_maquina][nome_sensor]
    critico = sensor_maquina['critico']
    alerta = sensor_maquina['atencao']
    unidade = sensor_maquina['unidade_medida']

    log_sensor = log(unidade)
    if valor_sensor >= critico:
        log_sensor.warning(f'CRÍTICO: Valor {valor_sensor}{unidade} LIMITE ULTRAPASSADO: {critico}{unidade}' )
        return {
            f'STATUS': 'CRÍTICO', 'mensagem': f'Valor crítico detectado: {valor_sensor}{unidade}, limite era: {critico}{unidade}'
        }

    elif valor_sensor >= alerta:
        log_sensor.info(f'ATENÇÃO: Valor {valor_sensor}{unidade} LIMITE ULTRAPASSADO: {critico}{unidade}')
        return {
            f'STATUS': 'ATENÇÃO', 'mensagem': f'Valor elevado detectado: {valor_sensor}{unidade}, limite de atenção era: {critico}{unidade}'
        }

    else:
        log_sensor.info(f'NORMAL: Valor {valor_sensor}{unidade}')
        return {
            f'STATUS': 'NORMAL', 'mensagem': f'Valor {valor_sensor}{unidade} está dentro dos conformes'
        }