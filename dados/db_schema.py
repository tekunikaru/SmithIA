import mariadb
from ferramentas import get_db_connection, execute_query, close_db_connection, log

def create_tables():
    db_log = log('DBSchema')
    try:
        # Table for raw sensor data
        execute_query("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                machine_id VARCHAR(255) NOT NULL,
                machine_type VARCHAR(255) NOT NULL,
                timestamp DATETIME NOT NULL,
                sensor_name VARCHAR(255) NOT NULL,
                sensor_value FLOAT NOT NULL
            );
        """)
        db_log.info("Table 'sensor_data' ensured to exist.")

        # Table for anomaly alerts
        execute_query("""
            CREATE TABLE IF NOT EXISTS sensor_alerts (
                alert_id INT AUTO_INCREMENT PRIMARY KEY,
                machine_id VARCHAR(255) NOT NULL,
                machine_type VARCHAR(255) NOT NULL,
                timestamp DATETIME NOT NULL,
                raw_data_window JSON NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'PENDING_DIAGNOSIS'
            );
        """
        )
        db_log.info("Table 'sensor_alerts' ensured to exist.")

        # Table for LLM diagnostics
        execute_query("""
            CREATE TABLE IF NOT EXISTS llm_diagnostics (
                diag_id INT AUTO_INCREMENT PRIMARY KEY,
                fk_alert_id INT NOT NULL,
                llm_response_text TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                FOREIGN KEY (fk_alert_id) REFERENCES sensor_alerts(alert_id)
            );
        """
        )
        db_log.info("Table 'llm_diagnostics' ensured to exist.")

    except mariadb.Error as e:
        db_log.error(f"Error creating tables: {e}")
        raise

if __name__ == "__main__":
    create_tables()
    print("Database schema completo.")
