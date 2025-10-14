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
<details><summary>Veja mais</summary>

```
.
├── config/                  
│ └── .env.example           # Copie para `.env` e informe chaves de LLM/embeddings
├── rag_data/                # Documentação bruta (RAG). (Formato padrão txt)
├── vetorize.py              # Script para criar vetores (FAISS).
├── requirements.txt         # Dependências Python.
├── Dockerfile               # Configuração do Container.
├── src/
│ ├── llm_provider.py        # Llm Gemini Google. Copie provedores extras se necessário.
│ ├── data_loader.py         # Carrega e divide documentos (semantic chunking).
│ ├── vector_store.py        # Inicializa/consulta o Vector Store (FAISS).
│ ├── prompts.py             # Definições e gestão de Engenharia de Prompt.
│ ├── handler.py             # Orquestra a pipeline RAG/LLM usada pelo servidor.
│ └── main.py                # Ponto de entrada (FastAPI - GET /health, POST /query).
│
└── ops/                     # Componentes Adicionais
  ├── providers/             # Opção de outros LLMs. Substitua src/llm_provider.py. 
  │ ├── openai_provider.py   # Inclua `langchain-openai>=0.2.0` em requirements.txt.
  │ ├── azure_provider.py    # Inclua `langchain-openai>=0.2.0`. Defina AZURE_* no .env.
  │ └── bedrock_provider.py  # Inclua `langchain-aws>=0.1.3` e configure credenciais AWS.
  ├── loaders/               # Opção de outros formatos. Substitua o data_loader.py
  │ ├── pdf_loader.py        # Inclua `PyPDF2>=3.0.0` em requirements.txt
  │ ├── docx_loader.py       # Inclua `python-docx>=0.8.11` em requirements.txt
  │ └── postgresql_loader.py # Inclua `psycopg[binary]>=3.2.0`. Defina `PG_DSN` no `.env`
  ├── tests/
  │ ├── test_rag_query.py    # Testes de Assertividade do RAG.
  │ └── test_load.py         # Teste de Carga/Latência (5.000 requisições/min).  
  ├── .git/                  # CI/CD (GitHub Actions) - incluir na pasta raiz
  │ └── deploy.yml
  ├── packages/              # Pacotes/Módulos proprietários (PyPI Interno/JFrog).
  ├── docker-compose.yml     # Desenvolvimento multi-container.
  └── iaac/                  # IaC (Terraform)
    ├── main.tf              # Configurações de Cloud (Ex: AWS, Azure, GCP).
    └── kubernetes/          # Configurações K8s.
        ├── deployment.yaml
        └── service.yaml
```
</details>
