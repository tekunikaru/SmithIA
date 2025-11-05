from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from datetime import datetime
import json
from ferramentas import executar_query, log

app = FastAPI(title="API de Detecção de Anomalias em Sensores",
              description="API para monitoramento de dados de sensores, detecção de anomalias e diagnósticos baseados em LLM.",
              version="1.0.0")

api_log = log('FastAPI')

@app.get("/api/sensores/ultimos", response_model=List[Dict[str, Any]])
async def obter_ultimos_dados_sensores(machine_id: str = None, limit: int = 100):
    """
    Recupera os dados mais recentes dos sensores, opcionalmente filtrados por machine_id.
    """
    query = """
        SELECT machine_id, machine_type, timestamp, sensor_name, sensor_value
        FROM sensor_data
        {}
        ORDER BY timestamp DESC
        LIMIT ?;
    """
    clausula_where = "WHERE machine_id = ?" if machine_id else ""
    params = (machine_id, limit) if machine_id else (limit,)

    try:
        data = executar_query(query.format(clausula_where), params, fetchall=True)
        if not data:
            raise HTTPException(status_code=404, detail="Nenhum dado de sensor encontrado.")
        return data
    except Exception as e:
        api_log.error(f"Erro ao buscar dados mais recentes dos sensores: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")

@app.get("/api/alertas/ultimos", response_model=List[Dict[str, Any]])
async def obter_ultimos_alertas(status: str = None, limit: int = 100):
    """
    Recupera os alertas de anomalia mais recentes, opcionalmente filtrados por status.
    """
    query = """
        SELECT alert_id, machine_id, machine_type, timestamp, status, raw_data_window
        FROM sensor_alerts
        {}
        ORDER BY timestamp DESC
        LIMIT ?;
    """
    clausula_where = "WHERE status = ?" if status else ""
    params = (status, limit) if status else (limit,)

    try:
        alerts = executar_query(query.format(clausula_where), params, fetchall=True)
        if not alerts:
            raise HTTPException(status_code=404, detail="Nenhum alerta encontrado.")
        # raw_data_window é armazenado como string JSON, fazer parse para resposta da API
        for alert in alerts:
            if 'raw_data_window' in alert and isinstance(alert['raw_data_window'], str):
                alert['raw_data_window'] = json.loads(alert['raw_data_window'])
        return alerts
    except Exception as e:
        api_log.error(f"Erro ao buscar alertas mais recentes: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")

@app.get("/api/diagnostico/{alert_id}", response_model=Dict[str, Any])
async def obter_diagnostico_por_id_alerta(alert_id: int):
    """
    Recupera o diagnóstico detalhado do LLM para um ID de alerta específico.
    """
    query = """
        SELECT d.diag_id, d.llm_response_text, d.timestamp, a.machine_id, a.machine_type
        FROM llm_diagnostics d
        JOIN sensor_alerts a ON d.fk_alert_id = a.alert_id
        WHERE d.fk_alert_id = ?;
    """
    try:
        diagnosis = executar_query(query, (alert_id,), fetchone=True)
        if not diagnosis:
            raise HTTPException(status_code=404, detail=f"Diagnóstico para o alerta ID {alert_id} não encontrado.")
        return diagnosis
    except Exception as e:
        api_log.error(f"Erro ao buscar diagnóstico para o alerta ID {alert_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")

if __name__ == "__main__":
    import uvicorn
    api_log.info("Iniciando aplicação FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8000)