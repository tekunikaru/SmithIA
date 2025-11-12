import time
from datetime import datetime
import lmstudio as lms
from ferramentas import(
    execute_query, verificar_sensor
)
from config_log import log


MODEL = 'qwen/qwen3-4b-2507'
POLL_INTERVAL = 1

logger = log('Orquestrador')

SYSTEM_PROMPT = """Você é o orquestrador de diagnósticos de equipamentos industriais.

FLUXO OBRIGATÓRIO:
1. AO RECEBER A RESPOSTA DO AGENTE1, VERIFICAR CADA SENSOR QUE ELE
APRESENTA:
   - Para cada sensor na resposta do Agente1, chame verificar_sensor(id_maquina, nome_sensor, valor_sensor)
   - Gere diagnóstico técnico: causa raiz + impacto + ações corretivas

2. SALVAR DIAGNÓSTICO: Use execute_query:
   INSERT INTO diagnostico_llm (fk_alerta_id, resposta_llm, timestamp)
   VALUES ([ID_ALERTA], '[SEU_DIAGNOSTICO]', NOW());
   
   IMPORTANTE: Escape aspas simples no diagnóstico usando '' (duas aspas simples)

3. ATUALIZAR STATUS:
   UPDATE alertas_sensor
   SET status = 'DIAGNOSTICO_CONCLUIDO'
   WHERE id_alerta = [ID_ALERTA];

BANCO DE DADOS:
- alertas_sensor: id_alerta, id_maquina, tipo_maquina, timestamp, janela_dados_bruto (JSON), status
- diagnostico_llm: id_diagnostico, fk_alerta_id, resposta_llm, timestamp

FERRAMENTAS:
- execute_query(consulta): MariaDB (use LIMIT, NOW())
- verificar_sensor(id_maquina, nome_sensor, valor_sensor): Validar valores críticos

REGRAS:
- Processe TODOS os alertas pendentes
- Use verificar_sensor nos sensores da resposta do agente1
- Salve o diagnóstico no diagnostico_llm antes de atualizar status
- Escape aspas simples no texto
- Confirme quantos alertas foram processados"""

def executar_orquestrador(agente1_conversa:lms.Chat):
    """Loop principal do orquestrador usando agente LLM"""
    
    logger.info("Iniciando Orquestrador com Agente LLM")
    
    # Inicializar modelo
    try:
        model = lms.llm(MODEL)
        options = lms.LlmPredictionConfig(
        temperature=0.98,
        top_k_sampling=0.0,
        top_p_sampling=0.37,
        min_p_sampling=0.0,
        repeat_penalty=0.98,
    )

    except Exception as e:
        logger.error(f" Erro ao carregar modelo: {e}")
        return
    
    # Lista de ferramentas disponíveis para o agente
    tools = [
        execute_query,
        verificar_sensor,
    ]
    
    while True:
        try:
            logger.info("Verificando alertas pendentes...")
            
            # Criar novo chat para cada ciclo
            
            agente1_conversa.add_system_prompt(SYSTEM_PROMPT)
            chat = agente1_conversa
            # Instrução para o agente
            user_message = """Análise os dados do equipamento que o agente1
            mandou

            1. Verifique todos os sensores
            2. Faça as seguintes atuações:
               - Gere o relatório formatado
               - Salve o diagnóstico em llm_diagnostics
               - Atualize o status do alerta da tabela alertas_sensor para 'DIAGNOSTICO_CONCLUIDO'

            Importante: Use as ferramentas SQL para buscar, salvar e atualizar dados."""
            
            chat.add_user_message(user_message)
            
            # Executar agente
            result = model.act(
                chat,
                tools,
                config=options,
                max_parallel_tool_calls=1
            )
            
            logger.info(f"Ciclo completo: {result.text[:100]}...")
            
            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("Orquestrador interrompido pelo usuário")
            break
        except Exception as e:
            logger.warning(f"Erro no ciclo: {e}")
            time.sleep(POLL_INTERVAL)
