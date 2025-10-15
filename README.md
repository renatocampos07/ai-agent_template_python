# 🤖 Template para Agentes de IA

* **Visão Geral:** Estrutura base para projetos de IA (*boilerplate*).
* **Objetivo:** Velocidade, portabilidade, escalabilidade.
* **Back-end:** *Python*, *LangChain* (orquestração e *RAG*).
* **Infra:** *Docker* para empacotamento/orquestração *Cloud Agnostic*.
---
1.  **Config:** Preencha `config/.env` com chaves e modelos (LLM/Embedding).
2.  **RAG:** Coloque docs em `rag_data/`. Crie vetores: `python vetorize.py`.
3.  **Build:** Gere a imagem final: `docker build -t agente-ia-pronto:latest .`
4.  **Deploy:** *Push* para **Container Registry**. Execute em *serverless* (Azure, AWS, GCP).
---    
* **Opcional**:  IaC **Terraform**, CI/CD **GitHub Actions**, **Docker Compose**, **K8s**.
* **Testes:** Pasta *`tests/`* com validações de integridade/performance. 
* **Frontend**: Livre (Ex. *React*, *Gradio*, RPA). 
* **Licença:** Uso livre, *MIT*. ️
---
```
.
├── config/                  
│ └── .env.example           # Modelo de variáveis de ambiente (LLM/embeddings)
│ └── .env                   # Arquivo real contendo chaves (oculto pelo .gitignore)
├── .gitignore               # Ignora arquivos/pastas locais e sensíveis
├── rag_data/                # Documentos brutos para RAG (padrão .txt)
├── vetorize.py              # Gera vetores FAISS do documentos
├── requirements.txt         # Lista de dependências (Python 3.12)
├── Dockerfile               # Configuração do Container (Docker/Rancher Desktop/WSL2)
└── src/
  ├── llm_provider.py        # Gestão da LLM/credenciais (padrão Gemini)
  ├── data_loader.py         # Carrega e divide documentos (Chuncking semântico)
  ├── vector_store.py        # Gerencia busca vetorial (Embedding/FAISS)
  ├── prompts.py             # Define templates/lógica para LLM (Engenharia de Prompt)
  ├── handler.py             # Orquestra a pipeline RAG/LLM 
  └── main.py                # Executa API (uvicorn src.main:app)(GET /health POST /query)
```
