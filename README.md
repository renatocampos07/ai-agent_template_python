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
* **Frontend**: Livre (Ex. *React*, RPA). 
* **Licença:** Uso livre, *MIT*. ️
---
<details><summary>Diretório</summary>


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
 
└── ops/                     # OPCIONAL (Complementos de Customização/infra)
  ├── providers/             # Outros provedores LLMs (Substitua llm_provider.py) 
  ├── loaders/               # Outros formatos .pdf/.docx/sql (Substitua data_loader.py)
  ├── tests/                 # Testes Assertividade do RAG/Carga/Latência 
  ├── packages/              # Pacotes/Módulos proprietários (PyPI Interno/JFrog)
  ├── poetry/                # Gerenciador de dependências do Poetry (.toml e .lock)
  ├── docker-compose/        # Desenvolvimento multi-container (.yml)
  ├── terraform/             # Infraestrutura como código (.tf)
  ├── kubernetes/            # Configurações K8s (.yaml)
  └── .git/                  # CI/CD GitHub Actions .yml (mover para pasta raiz)

```
</details>

<details><summary>Demonstração</summary>

**Azure:** Com a imagem 
- Build da imagem: `docker build -t <nomecontainer>.azurecr.io/app:latest .`
- Push para Registry: `docker login <nomecontainer>.azurecr.io -u <usuario> -p <senha>` e `docker push <nomecontainer>.azurecr.io/app:latest`
- Criar ACI: `az container create --resource-group <grupo> --name <nomeagente>-ia-demo --image <nomecontainer>.azurecr.io/app:latest --registry-login-server <nomecontainer>.azurecr.io --registry-username <usuario> --registry-password <senha> --dns-name-label <nomeagente>-ia-demo --ports 8000`
- Testar na Cloud Shell: `Invoke-WebRequest http://<ip-ou-dns>:8000/health` e `Invoke-RestMethod -Uri "http://<ip-ou-dns>:8000/query" -Method Post -Body '{"question":"Sua pergunta"}' -ContentType "application/json"`

![](/demo_azure.png)

</details>