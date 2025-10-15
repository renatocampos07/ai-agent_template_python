# Em desenvolvimento
Complementos opcionais para customização e infraestrutura

```
└── ops/                     
  ├── providers/             # Outros provedores LLMs (Substitua llm_provider.py) 
  ├── loaders/               # Outros formatos .pdf/.docx/sql (Substitua data_loader.py)
  ├── tests/                 # Testes Assertividade do RAG/Carga/Latência 
  ├── packages/              # Pacotes/Módulos proprietários (PyPI Interno/JFrog)
  ├── poetry/                # Gerenciador de dependências do Poetry (.toml e .lock)
  ├── docker-compose/        # Desenvolvimento multi-container (.yml)
  ├── terraform/             # Infraestrutura como código (.tf)
  ├── kubernetes/            # Configurações K8s (.yaml)
  ├── frontend/              # Interface web (Gradio)
  └── .git/                  # CI/CD GitHub Actions .yml (mover para pasta raiz)
```