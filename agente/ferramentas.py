import mariadb
from config_log import log
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def obter_conexao_bd():
    """
    Estabelece e retorna uma conexão com o banco de dados MariaDB.
    Detalhes da conexão são carregados das variáveis de ambiente.
    """
    try:
        conn = mariadb.connect(
            user=os.getenv("DB_USER", "xxxx"),
            password=os.getenv("DB_PASSWORD", ""),
            host=os.getenv("DB_HOST", "xxxxxx1"),
            port=int(os.getenv("DB_PORT", 'xxxx')),
            database=os.getenv("DB_NAME", "project_smith")
        )
        return conn
    except mariadb.Error as e:
        db_log = log('Database')
        db_log.error(f"Erro ao conectar na plataforma MariaDB: {e}")
        raise

def executar_query(query: str, params: tuple = None, fetchone: bool = False, fetchall: bool = False):
    """
    Executa uma query SQL e retorna o resultado.
    Gerencia automaticamente a conexão e o cursor.
    """
    conn = None
    cursor = None
    try:
        conn = obter_conexao_bd()
        cursor = conn.cursor(dictionary=True) # Retorna linhas como dicionários
        cursor.execute(query, params)
        conn.commit()
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
        return None
    except mariadb.Error as e:
        db_log = log('Database')
        db_log.error(f"Erro ao executar query: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fechar_conexao_bd(conn):
    """
    Fecha a conexão com o banco de dados.
    """
    if conn:
        conn.close()

def verificar_temperatura(temperature: float) -> dict:
    """
    Verifica se o valor da temperatura é crítico, alto ou normal.
    Args:
        temperature (float): A temperatura a ser analisada.
    Returns:
        dict: status e mensagem
    """
    temperatura = log('Temperatura')
    if temperature >= 88:
        temperatura.warning('Temperatura crítica, tome cuidado!')
        return {"status": "CRITICAL", "message": "Temperatura crítica - Superaquecimento detectado. Risco de dano permanente."}
    elif temperature >= 70:
        temperatura.info('Temperatura alta demais!')
        return {"status": "ATTENTION", "message": "Temperatura elevada - Sistema de resfriamento pode estar comprometido."}
    else:
        temperatura.info('Temperatura normal!')
        return {"status": "NORMAL", "message": f"{temperature}°C está dentro do esperado"}


def verificar_vibracao(vibration: float) -> dict:
    """
    Verifica se o valor da vibração é crítico, acima do normal ou normal.
    Args:
        vibration (float): A vibração a ser analisada.
    Returns:
        dict: status e mensagem
    """
    vibracao = log('Vibração')
    if vibration >= 7.1:
        vibracao.warning('Vibração crítica detectada, tome cuidado!')
        return {"status": "CRITICAL", "message": "Vibração crítica detectada - Risco iminente de falha mecânica. Pare a máquina imediatamente."}
    elif vibration >= 4.5:
        vibracao.info('Vibração acima do normal')
        return {"status": "ATTENTION", "message": "Vibração acima do normal - Possível desbalanceamento ou desgaste de rolamento."}
    else:
        vibracao.info('Vibração está normal')
        return {"status": "NORMAL", "message": f"{vibration} mm/s está dentro do esperado"}



def verificar_corrente(current: int) -> dict:
    """
    Verifica se o valor da corrente é crítico, alto ou normal.
    Args:
        current (int): A corrente a ser analisada.
    Returns:
        dict: status e mensagem
    """
    corrente = log('Corrente elétrica')
    if current >= 45:
        corrente.warning('Corrente elétrica está crítica, cuidado!')
        return {"status": "CRITICAL", "message": "Corrente crítica - Sobrecarga severa do motor. Risco de queima do equipamento."}
    elif current >= 38:
        corrente.info('Corrente elétrica elevada')
        return {"status": "ATTENTION", "message": "Corrente elevada - Motor operando acima da capacidade nominal."}
    else:
        corrente.info('Corrente elétrica normal')
        return {"status": "NORMAL", "message": f"{current} A está dentro do esperado"}



def verificar_rpm(rpm: int) -> dict:
    """
    Verifica se o valor do rpm é crítico, anormal ou normal.
    Args:
        rpm (int): o rpm a ser analisado.
    Returns:
        dict: status e mensagem
    """
    rpm_log = log('Rpm')
    if rpm <= 800 or rpm >= 1300:
        rpm_log.warning('Rotação crítica, cuidado!')
        return {"status": "CRITICAL", "message": "Rotação crítica - Motor fora da faixa operacional segura. Risco de dano mecânico."}
    elif rpm < 900 or rpm >= 1200:
        rpm_log.info('Rotação está anormal!')
        return {"status": "ATTENTION", "message": "Rotação anormal - Verifique carga e condições de operação."}
    else:
        rpm_log.info('rpm está normal')
        return {"status": "NORMAL", "message": f"{rpm} RPM está dentro do esperado"}


def verificar_pressao(pressure: int) -> dict:
    """
    Verifica se a pressão é crítica, baixa ou normal.
    Args:
        pressure (int): A pressão a ser analisada.
    Returns:
        dict: status e mensagem
    """
    pressao = log('Pressão')
    if pressure <= 80:
        pressao.warning('Pressão crítica, cuidado!')
        return {"status": "CRITICAL", "message": "Pressão crítica - Falha no sistema hidráulico. Possível vazamento ou bomba danificada."}
    elif pressure <= 90:
        pressao.info('Pressão está baixa')
        return {"status": "ATTENTION", "message": "Pressão baixa - Monitore o sistema hidráulico para vazamentos."}
    else:
        pressao.info('Pressão está normal')
        return {"status": "NORMAL", "message": f"{pressure} bar está dentro do esperado"}