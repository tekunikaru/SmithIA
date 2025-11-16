import time
import json
from datetime import datetime, timedelta
import lmstudio as lms
from agente.tools.ferramentas import executar_query, log

orchestrator_log = log('Orquestrador')

main_model = 'qwen/qwen3-4b-2507' # LLM para diagnóstico detalhado

# Inicializar modelos do LM Studio
try:
    llm_model = lms.llm(main_model)
    orchestrator_log.info(f"Modelo LLM carregado com sucesso: {main_model}")
except Exception as e:
    orchestrator_log.error(f"Falha ao carregar modelo LLM {main_model}: {e}. Certifique-se de que o LM Studio está rodando e o modelo está carregado.")
    llm_model = None # Define como None se o carregamento falhar

def obter_alertas_pendentes():
    """
    Busca alertas com status 'PENDING_DIAGNOSIS'.
    """
    query = "SELECT * FROM sensor_alerts WHERE status = 'PENDING_DIAGNOSIS';"
    try:
        alerts = executar_query(query, fetchall=True)
        return alerts
    except Exception as e:
        orchestrator_log.error(f"Erro ao buscar alertas pendentes: {e}")
        return []

def obter_dados_historicos(machine_id: str, tempo_final: datetime, janela_tempo_horas: int = 2):
    """
    Busca dados históricos de sensores para uma determinada máquina.
    """
    tempo_inicial = tempo_final - timedelta(hours=janela_tempo_horas)
    query = """
        SELECT machine_id, machine_type, timestamp, sensor_name, sensor_value
        FROM sensor_data
        WHERE machine_id = ? AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp DESC;
    """
    try:
        data = executar_query(query, (machine_id, tempo_inicial, tempo_final), fetchall=True)
        return data
    except Exception as e:
        orchestrator_log.error(f"Erro ao buscar dados históricos para {machine_id}: {e}")
        return []

def gerar_prompt_llm(dados_alerta: dict, dados_historicos: list) -> str:
    """
    Gera um prompt detalhado para o LLM Qwen 4b.
    """
    machine_id = dados_alerta['machine_id']
    janela_dados_brutos = json.loads(dados_alerta['raw_data_window'])

    # Formatar janela_dados_brutos para o prompt
    str_dados_anomalia = json.dumps(janela_dados_brutos, indent=2)

    # Formatar dados_historicos para o prompt
    str_dados_historicos = json.dumps(dados_historicos, indent=2)

    prompt_qwen_4b = f"""
[INÍCIO DO PROMPT PARA QWEN 4B] 

**Função:** Você é um Engenheiro de Manutenção Preditiva e Analista de Sistemas Sênior. 

**Contexto:** Um alerta de anomalia foi gerado automaticamente para a máquina {machine_id}. O sistema de monitoramento (Qwen 0.6b) classificou a seguinte janela de dados como 'ANOMALO'. 

**Dados da Anomalia (Janela Atual):** 
```json
{str_dados_anomalia}
```

**Dados Históricos (Contexto Adicional - últimas 2 horas):** 
```json
{str_dados_historicos}
```

**Sua Tarefa (Dividida em Duas Partes):** 

1.  **Diagnóstico Provável:** 
    * Analise os dados da anomalia em contraste com os dados históricos. 
    * Qual é a causa provável desta anomalia? (Ex: "Superaquecimento do sensor T-02", "Vibração inconsistente indicando desalinhamento", "Padrão de dados sugere falha iminente no componente X"). 
    * Seja específico e técnico. 

2.  **Recomendação de Ação:** 
    * Com base no seu diagnóstico, qual é o plano de ação imediato recomendado? 
    * (Ex: "1. Reduzir a carga da máquina em 50%. 2. Enviar equipe de manutenção para inspecionar o rolamento T-02. 3. Agendar calibração do sensor de vibração."). 
    * Seja claro e direto. 

**Formato da Resposta:** 
Responda APENAS com o diagnóstico e a recomendação, sem frases introdutórias. 

[FIM DO PROMPT PARA QWEN 4B]
"""
    return prompt_qwen_4b

def obter_diagnostico_llm(prompt: str) -> str:
    """
    Obtém um diagnóstico detalhado do LLM Qwen 4b.
    """
    if not llm_model:
        orchestrator_log.error("Modelo LLM não carregado. Não é possível obter diagnóstico.")
        return "Modelo LLM Não Disponível"

    try:
        chat = lms.Chat(system_prompt="Você é um engenheiro especialista em manutenção preditiva. Forneça um diagnóstico detalhado e ações recomendadas com base nos dados de sensores fornecidos.")
        chat.add_user_message(prompt)
        result = llm_model.act(chat, config=lms.LlmPredictionConfig(temperature=0.7, max_tokens=500))
        return result.text.strip()
    except Exception as e:
        orchestrator_log.error(f"Erro ao obter diagnóstico do LLM: {e}")
        return f"Erro durante diagnóstico do LLM: {e}"

def armazenar_diagnostico_llm(alert_id: int, texto_resposta_llm: str):
    """
    Armazena o diagnóstico do LLM na tabela llm_diagnostics.
    """
    query = """
        INSERT INTO llm_diagnostics (fk_alert_id, llm_response_text, timestamp)
        VALUES (?, ?, ?);
    """
    try:
        executar_query(query, (alert_id, texto_resposta_llm, datetime.now()))
        orchestrator_log.info(f"Diagnóstico do LLM armazenado para alert_id {alert_id}.")
    except Exception as e:
        orchestrator_log.error(f"Erro ao armazenar diagnóstico do LLM para alert_id {alert_id}: {e}")

def atualizar_status_alerta(alert_id: int, status: str):
    """
    Atualiza o status de um alerta na tabela sensor_alerts.
    """
    query = "UPDATE sensor_alerts SET status = ? WHERE alert_id = ?;"
    try:
        executar_query(query, (status, alert_id))
        orchestrator_log.info(f"Status do alerta {alert_id} atualizado para {status}.")
    except Exception as e:
        orchestrator_log.error(f"Erro ao atualizar status para o alerta {alert_id}: {e}")

def executar_servico_orquestrador():
    orchestrator_log.info("Iniciando Serviço Orquestrador...")
    while True:
        alerts = obter_alertas_pendentes()
        if alerts:
            orchestrator_log.info(f"Encontrados {len(alerts)} alertas pendentes.")
            for alert in alerts:
                alert_id = alert['alert_id']
                machine_id = alert['machine_id']
                alert_timestamp = alert['timestamp']

                orchestrator_log.info(f"Processando alerta {alert_id} para máquina {machine_id}.")

                # Buscar dados históricos para contexto
                dados_historicos = obter_dados_historicos(machine_id, alert_timestamp, janela_tempo_horas=2)

                # Gerar prompt para LLM
                llm_prompt = gerar_prompt_llm(alert, dados_historicos)

                # Obter diagnóstico do LLM
                texto_diagnostico_llm = obter_diagnostico_llm(llm_prompt)

                # Armazenar diagnóstico e atualizar status do alerta
                armazenar_diagnostico_llm(alert_id, texto_diagnostico_llm)
                atualizar_status_alerta(alert_id, "DIAGNOSED")
        else:
            orchestrator_log.info("Nenhum alerta pendente encontrado.")

        time.sleep(15) # Verificar novos alertas a cada 15 segundos

if __name__ == "__main__":
    executar_servico_orquestrador()