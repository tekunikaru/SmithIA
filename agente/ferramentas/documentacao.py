from lmstudio import ToolFunctionDef
from agente.regras_sensores import sensores


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