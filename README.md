# 🤖 Template para Agentes de IA
---
* **Visão Geral:** Estrutura base para projetos de IA (*boilerplate*).
* **Objetivo:** Velocidade, portabilidade, escalabilidade.
* **Back-end:** *Python*, *LangChain* (orquestração e *RAG*).
* **Infra:** *Docker* para empacotamento/orquestração *Cloud Agnostic*.
---
1.  **Config:** Preencha `config/.env` com chaves e modelos (LLM/Embedding).
2.  **RAG:** Coloque docs em `rag_data/`. Crie vetores: `python vetorize.py`.
3.  **Build:** Gere a imagem final: `docker build -t agente-ia-pronto:latest .`
4.  **Deploy:** Faça o *Push* para o **Container Registry** (ACR, ECR, GCR, ICR).
---    
* **Opcional**:  IaC **Terraform**, CI/CD **GitHub Actions**, **Docker Compose**, **K8s**.
* **Testes:** Pasta *`tests/`* com validações de integridade/performance. 
* **Frontend**: Livre (Ex. *React*, RPA). 
* **Licença:** Uso livre, *MIT*. ️
---
```
.
├── src/
│ ├── data_loader.py         # Carrega e divide documentos (semantic chunking).
│ ├── vector_store.py        # Inicializa/consulta o Vector Store (FAISS).
│ ├── prompts.py             # Definições e gestão de Engenharia de Prompt.
│ ├── llm_provider.py        # Conexão com LLM (Bedrock, Azure Foundry, OpenAI).
│ └── main.py                # Ponto de Entrada: HTTP Request e RAG.
│
├── ops/                     # Recursos Opcionais
│ ├── ci/                    # CI/CD (GitHub Actions)
│ │ └── deploy.yml
│ ├── iaac/                  # IaC (Terraform)
│ │ ├── main.tf              # Configurações de Cloud (Ex: AWS, Azure).
│ │ └── kubernetes/          # Configurações K8s.
│ │     ├── deployment.yaml
│ │     └── service.yaml
│ ├── tests/                 
│ │ ├── test_rag_query.py    # Testes de Assertividade do RAG.
│ │ └── test_load.py         # Teste de Carga/Latência (5.000 requisições/min).
│ ├── packages/              # Pacotes/Módulos proprietários (PyPI Interno/JFrog).
│ └── docker-compose.yml     # Desenvolvimento multi-container.
│
├── rag_data/                # Documentação bruta (RAG).
├── config/
│ └── .env.example
├── requirements.txt         # Dependências Python.
├── vetorize.py              # Script para criar vetores (FAISS).
└── Dockerfile               # Configuração do Container.
```
