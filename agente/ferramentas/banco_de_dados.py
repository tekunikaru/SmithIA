from lmstudio import ToolFunctionDef
import mariadb
from agente.segredos import *

def _consulta_sql(consulta: str) -> list:
    """
    Executa comandos SQL no banco de dados SQL Server local.
    """
    conn = mariadb.connect(
        user=BD_USUARIO,
        host=BD_HOST,
        port=BD_PORTA,
        password=BD_SENHA,
        database="project_smith"
    )
    cur = conn.cursor()
    cur.execute(consulta)
    resultados = cur.fetchall()
    return resultados

consulta_sql = ToolFunctionDef.from_callable(_consulta_sql)