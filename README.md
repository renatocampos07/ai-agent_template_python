# 🤖 Template para Agentes de IA

* **Visão Geral:** Estrutura base para projetos de IA (*boilerplate*).
* **Objetivo:** Velocidade, portabilidade, escalabilidade.
* **Back-end:** *Python*, *LangChain* (orquestração e *RAG*).
* **Infra:** *Docker* para empacotamento/orquestração *Cloud Agnostic*.
---
1.  **Config:** Preencha `config/.env` com chaves e modelos (LLM/Embedding).
2.  **RAG:** Coloque docs em `rag_data/`. Crie vetores: `python vetorize.py`.
3.  **Build:** Gere a imagem final: `docker build -t agente-ia-pronto:latest .`
4.  **Deploy:** *Push* para **Container Registry**. Execute em *serverless* (Azure, AWS).
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
</details>

<details><summary>Opcionais</summary>

```
└── ops/                     # Complementos para customização e infra (Em desenvolvimento)
  ├── providers/             # Outros provedores LLMs (Substitua llm_provider.py) 
  ├── loaders/               # Outros formatos .pdf/.docx/sql (Substitua data_loader.py)
  ├── agent_roles/           # Outros Multi-Agentes especializados (Substitua prompts.py)
  ├── tests/                 # Testes Assertividade do RAG/Carga/Latência 
  ├── packages/              # Pacotes/Módulos proprietários (PyPI Interno/JFrog)
  ├── poetry/                # Gerenciador de dependências do Poetry (.toml e .lock)
  ├── docker-compose/        # Desenvolvimento multi-container (.yml)
  ├── terraform/             # Infraestrutura como código (.tf)
  ├── frontend/              # Interface web (Gradio)
  ├── kubernetes/            # Configurações K8s (.yaml)
  └── .git/                  # CI/CD GitHub Actions .yml (mover para pasta raiz)

```
</details>

<details><summary>Demonstração</summary>

#### Este guia mostra como subir e testar o agente de IA no Azure usando Cloud Shell
![](/demo_azure.png)
---
- Criar Resource Group: `az group create --name agente-ia-gr --location eastus`
- Criar ACR: `az acr create --resource-group agente-ia-gr --name agenteiacontainer --sku Standard`
- Criar imagem: `docker build -t agenteiacontainer.azurecr.io/app:latest .`
- Login ACR: `docker login agenteiacontainer.azurecr.io -u -p`
- Push imagem: `docker push agenteiacontainer.azurecr.io/app:latest`
- Criar ACI: `az container create --resource-group agente-ia-gr --name aci-agente-ia --image agenteiacontainer.azurecr.io/app:latest --registry-login-server agenteiacontainer.azurecr.io --registry-username --registry-password --dns-name-label aci-agente-ia --ports 8000`
- Testar saúde: `Invoke-WebRequest http://:8000/health`
- Testar consulta: `Invoke-RestMethod -Uri "http://:8000/query" -Method Post -Body '{"question":"Sua pergunta"}' -ContentType "application/json"`
</details>
