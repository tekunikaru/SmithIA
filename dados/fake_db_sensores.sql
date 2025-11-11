CREATE TABLE IF NOT EXISTS dados_sensor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_maquina VARCHAR(50) NOT NULL,
    tipo_maquina VARCHAR(50) NOT NULL,
    timestamp DATETIME NOT NULL,
    nome_sensor VARCHAR(50) NOT NULL,
    valor_sensor FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS alertas_sensor (
    id_alerta INT AUTO_INCREMENT PRIMARY KEY,
    id_maquina VARCHAR(50) NOT NULL,
    tipo_maquina VARCHAR(50) NOT NULL,
    timestamp DATETIME NOT NULL,
    janela_dados_bruto JSON NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'DIAGNOSTICO_PENDENTE'
);

