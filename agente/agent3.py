from lmstudio import *
from dataclasses import dataclass
from typing import Iterable
from enum import Enum
from agente.ferramentas.documentacao import verificar_sensor
from agente.configs.config_inferencia import MidnightEnigma

@dataclass
class AgentConfig:
    modelo_supervisor =  'qwen/qwen3-4b-2507'
    modelo_rascunho   =  'qwen/qwen3-0.6b'
    config_inferencia =  MidnightEnigma()

@dataclass
class Agent3:
    class Tipo(Enum):
        PRIMARIO   = 0
        SECUNDARIO = 1
    config: AgentConfig
    tools : Iterable[ToolFunctionDef]
    chat  : Chat = Chat()
    modo  : Tipo

    def limpar_contexto()->None:
        pass

# PROMPT DO SISTEMA
system_prompt = '''<|BOS|> de monitoramento de equipamentos que usa ferramentas para analisar dados de sensores.

FLUXO DE TRABALHO OBRIGATÓRIO:

1. BUSCAR DADOS: Use `execute_query` com esta consulta (linha única, sem quebras):
   WITH UltimosSensores AS (SELECT id_maquina, tipo_maquina, nome_sensor, valor_sensor, timestamp, ROW_NUMBER() OVER(PARTITION BY nome_sensor ORDER BY timestamp DESC) as rn FROM dados_sensor WHERE id_maquina = '[NOME_DA_MAQUINA]') SELECT id_maquina, tipo_maquina, nome_sensor, valor_sensor, timestamp FROM UltimosSensores WHERE rn = 1;

2. ITERAR E VERIFICAR: A consulta retorna MÚLTIPLAS LINHAS. Chame `verificar_sensor(id_maquina, nome_sensor, valor_sensor)` para CADA linha. Anote o status de cada sensor.

3. REGISTRAR ALERTA: Se PELO MENOS UM sensor retornou "crítico", execute (linha única):
   INSERT INTO alertas_sensor (id_maquina, tipo_maquina, timestamp, janela_dados_bruto, status) VALUES ('[ID_MAQUINA]', '[TIPO_MAQUINA]', '[TIMESTAMP_MAIS_RECENTE]', 'Alerta automático', 'DIAGNOSTICO_PENDENTE');

4. DIAGNÓSTICO FINAL: Forneça um diagnóstico consolidado com status de cada sensor e se registrou alerta.

BANCO DE DADOS: MariaDB
- dados_sensor: id, id_maquina, tipo_maquina, timestamp, nome_sensor, valor_sensor
- alertas_sensor: id_alerta, id_maquina, tipo_maquina, timestamp, janela_dados_bruto, status

FERRAMENTAS:
- `execute_query(consulta)`: SQL em linha única, sem \n
- `verificar_sensor(id_maquina, nome_sensor, valor_sensor)`: Retorna status do sensor

IMPORTANTE: 
Sempre verifique TODOS os sensores. 
Consultas SQL em linha única.
Coloque o registro no alertas sensor só no final e SOMENTE se houver algum sensor crítico

'''

# Criar modelo
model = lms.llm(main_mode0l)

options = 

# CRIAR CHAT
chat = lms.Chat(system_prompt)

# Mensagem do usuário
user_message = f"""Analise os dados do equipamento CAF-98-001 

Lembre-se:

1. Verificar todos os sensores
2. Dar o diagnóstico"""

chat.add_user_message(user_message)

def on_round_start(round_index):
    print(f"\n{'='*60}")
    print(f" RODADA {round_index} INICIADA")
    print('='*60)

def on_round_end(round_index):
    print(f"\n{'='*60}")
    print(f"✓ RODADA {round_index} CONCLUÍDA")
    print('='*60)

def on_prediction_completed(round_result):
    print(f"\n  Predição da rodada {round_result.round_index} concluída")
    if hasattr(round_result, 'tool_calls') and round_result.tool_calls:
        print(f"     Modelo solicitou {len(round_result.tool_calls)} ferramenta(s)")

def on_message(message):
    print(f"\n Mensagem: {type(message).__name__}")

def on_prediction_fragment(fragment, round_index):
    print(fragment.content, end='', flush=True)

# LISTA DE FERRAMENTAS
tools = [
    verificar_sensor,
    execute_query
]

print("="*60)
print("INICIANDO EXECUÇÃO DO AGENTE")
print("="*60)


try:
    result = model.act(
        chat,
        tools,
        config=options,
        on_round_start=on_round_start,
        on_round_end=on_round_end,
        on_prediction_completed=on_prediction_completed,
        on_message=on_message,
        on_prediction_fragment=on_prediction_fragment,
        max_parallel_tool_calls=1  
    )
    
    print("\n" + "="*60)               
    print(" RESULTADO FINAL:")
    print("="*60)
    print(result)

except Exception as e:
    print(f"\n ERRO: {e}")
    import traceback
    traceback.print_exc()

if __name__ == '__main__':
    