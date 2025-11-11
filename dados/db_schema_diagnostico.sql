CREATE TABLE IF NOT EXISTS diagnostico_llm (
    id_diagnostico INT AUTO_INCREMENT PRIMARY KEY,
    fk_alerta_id INT NOT NULL,
    resposta_llm TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (fk_alerta_id) REFERENCES alertas_sensor(alerta_id)
);