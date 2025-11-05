# Sistema de Diagnóstico de Anomalias em Sensores

Este projeto implementa um sistema de monitoramento e diagnóstico de anomalias em tempo real para dados de sensores industriais. Ele utiliza modelos de linguagem (Qwen 0.6b e Qwen 4b) para detecção e diagnóstico aprofundado, com os dados armazenados em MariaDB e expostos via uma API FastAPI.

## Arquitetura

O sistema é composto por quatro módulos principais:

1.  **Geração de Dados (`script.py`):** Simula dados de sensores para diferentes tipos de máquinas e os salva em arquivos CSV.
2.  **Ingestão de Dados (`data_ingestor.py`):** Lê os dados dos CSVs gerados e os insere no banco de dados MariaDB.
3.  **Serviço de Detecção de Anomalias (`detector_service.py`):** Monitora o MariaDB, aplica um pré-filtro e utiliza um modelo SLM (Qwen 0.6b) para classificar janelas de dados como 'NORMAL' ou 'ANOMALO'. Alertas são armazenados no banco de dados.
4.  **Orquestrador de Diagnóstico (`orchestrator.py`):** Monitora novos alertas, coleta dados históricos e utiliza um modelo LLM (Qwen 4b) para gerar diagnósticos detalhados e recomendações. Os diagnósticos são armazenados no banco de dados.
5.  **API (`main.py`):** Uma API RESTful construída com FastAPI para expor os dados de sensores, alertas e diagnósticos.

## Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes softwares instalados:

*   **Python 3.8+**
*   **MariaDB Server:** Certifique-se de que o MariaDB esteja em execução e acessível. Crie um banco de dados chamado `project_smith` (ou o nome configurado no `.env`).
*   **LM Studio:** Para executar os modelos Qwen localmente. Baixe e instale o LM Studio e carregue os modelos `qwen3-0.6b` e `qwen/qwen3-4b-2507` (ou modelos equivalentes que você deseja usar).

## Configuração

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd Smith
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto com as seguintes informações do seu banco de dados MariaDB:
    ```
    DB_USER=root
    DB_PASSWORD=
    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_NAME=project_smith
    ```
    *Atenção:* Altere `DB_PASSWORD` se você tiver uma senha para o seu usuário `root` do MariaDB.

## Como Executar

Siga a ordem abaixo para iniciar o sistema:

1.  **Inicie o LM Studio:**
    Abra o LM Studio e certifique-se de que os modelos `qwen3-0.6b` e `qwen/qwen3-4b-2507` estejam carregados e o servidor local esteja em execução. O `detector_service.py` e `orchestrator.py` tentarão se conectar a ele.

2.  **Crie as tabelas do banco de dados:**
    ```bash
    python db_schema.py
    ```
    Isso criará as tabelas `sensor_data`, `sensor_alerts` e `llm_diagnostics` no seu banco de dados `project_smith`.

3.  **Gere os dados simulados:**
    ```bash
    python script.py
    ```
    Este script criará arquivos CSV com dados simulados de sensores.

4.  **Ingira os dados no MariaDB:**
    ```bash
    python data_ingestor.py
    ```
    Este script lerá os CSVs e populará a tabela `sensor_data`.

5.  **Inicie o Serviço de Detecção de Anomalias:**
    ```bash
    python detector_service.py
    ```
    Este serviço começará a monitorar os dados e gerar alertas.

6.  **Inicie o Orquestrador de Diagnóstico:**
    ```bash
    python orchestrator.py
    ```
    Este serviço começará a processar os alertas e gerar diagnósticos LLM.

7.  **Inicie a API FastAPI:**
    ```bash
    python main.py
    ```
    A API estará disponível em `http://127.0.0.1:8000` (ou a porta configurada).

    *   **Documentação da API:** Acesse `http://127.0.0.1:8000/docs` para a documentação interativa (Swagger UI).

## Endpoints da API

*   **`GET /api/sensors/latest`**
    *   **Descrição:** Recupera os dados de sensores mais recentes.
    *   **Parâmetros de Query:**
        *   `machine_id` (opcional): Filtra por ID da máquina.
        *   `limit` (opcional, padrão: 100): Número máximo de registros a retornar.

*   **`GET /api/alerts/latest`**
    *   **Descrição:** Recupera os alertas de anomalia mais recentes.
    *   **Parâmetros de Query:**
        *   `status` (opcional): Filtra por status do alerta (ex: `PENDING_DIAGNOSIS`, `DIAGNOSED`).
        *   `limit` (opcional, padrão: 100): Número máximo de registros a retornar.

*   **`GET /api/diagnosis/{alert_id}`**
    *   **Descrição:** Recupera o diagnóstico detalhado do LLM para um `alert_id` específico.

## Tratamento de Erros e Estabilidade

O sistema inclui logging básico via `config_log.py` para monitorar o fluxo e identificar problemas. Recomenda-se implementar tratamento de erros mais robusto (`try...except`) em todas as interações com o banco de dados e chamadas aos modelos LLM para garantir a resiliência do sistema. Pontos chave para melhoria incluem:

*   **Conexões de Banco de Dados:** Adicionar retries para falhas de conexão e consultas.
*   **Chamadas LLM:** Implementar timeouts e retries para chamadas aos modelos Qwen.
*   **Validação de Dados:** Adicionar validação de dados de entrada em todos os módulos para prevenir erros.
*   **Monitoramento:** Integrar com um sistema de monitoramento para alertas em caso de falhas de serviço.

## Depuração

Se encontrar erros, verifique os logs gerados em `claudio.log` e a saída dos terminais de cada serviço. O LM Studio também fornece logs detalhados sobre as interações com os modelos LLM.
