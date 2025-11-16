from lmstudio import ToolFunctionDef
import mariadb
from agente.configs.segredos import *
from agente.utils.logger import log

def _consulta_sql(consulta: str) -> list:
    """
    Executa comandos SQL no banco de dados SQL Server local.
    """
    log_sensor = log("[FERRAMENTA] Consulta SQL")
    try:
        conn = mariadb.connect(
            user=BD_USUARIO,
            host=BD_HOST,
            port=BD_PORTA,
            password=BD_SENHA,
            database=BD_BASE
        )
        cur = conn.cursor()
        cur.execute(consulta)
        resultados = cur.fetchall()
        return resultados
    except:
        log_sensor.erro("Erro na consulta")
        return ["Erro na consulta"]

consulta_sql = ToolFunctionDef.from_callable(_consulta_sql)