# syntax=docker/dockerfile:1.6
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Garante que a pasta config existe
RUN mkdir -p config

COPY src ./src
COPY vetorize.py ./
COPY rag_data ./rag_data
COPY config/.env.example ./config/.env.example

# Porta padrão do servidor HTTP minimalista
EXPOSE 8000

# Variável de controle para auto geração do vector store (opcional)
ENV AUTO_BUILD_VECTOR_STORE=false

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
