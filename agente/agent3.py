import lmstudio as lms
from ferramentas import (
    verify_current, verify_pressure, verify_rpm, 
    verify_temperature, verify_vibration, execute_query
)

# Modelos
draft_model = 'qwen3-0.6b'
main_model = 'qwen/qwen3-4b-2507'

# PROMPT DO SISTEMA
system_prompt = """Você é uma IA de monitoramento de equipamentos que usa ferramentas para analisar dados de sensores.

FLUXO DE TRABALHO:
1. Verificar cada sensor usando as ferramentas de verificação
2. Fornecer diagnóstico final

BANCO DE DADOS: tabela anomalo
Colunas: id_maquina, timestamp, temperatura, vibracao, corrente, rpm, pressao

FERRAMENTAS DISPONÍVEIS:
- execute_query(consulta): Executar SQL
- verify_temperature(temperature): Verificar temperatura
- verify_vibration(vibration): Verificar vibração  
- verify_current(current): Verificar corrente
- verify_rpm(rpm): Verificar RPM
- verify_pressure(pressure): Verificar pressão

IMPORTANTE: Sempre use TODAS as ferramentas antes de dar o diagnóstico."""

# Criar modelo
model = lms.llm(main_model)

options = lms.LlmPredictionConfig(
        temperature=0.98,
        top_k_sampling=0.0,
        top_p_sampling=0.37,
        min_p_sampling=0.0,
        repeat_penalty=0.98,
        draft_model=draft_model
    )

# CRIAR CHAT
chat = lms.Chat(system_prompt)

# Mensagem do usuário
user_message = f"""Analise estes dados do equipamento:

Máquina: 3
Hora: 2025-10-27 14:31:00
Temperatura: 60°C
Vibração: 3.1 mm/s
Corrente: 32 A
RPM: 1100
Pressão: 30 bar

Lembre-se:
1. INSERT no banco de dados primeiro
2. Verificar todos os 5 sensores
3. Dar o diagnóstico"""

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
    execute_query,     
    verify_temperature, 
    verify_vibration, 
    verify_current, 
    verify_rpm, 
    verify_pressure
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