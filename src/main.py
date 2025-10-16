"""FastAPI server exposing the RAG handler endpoints."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Query, Request  # type: ignore[import]
from fastapi.responses import JSONResponse  # type: ignore[import]

from .data_loader import chunk_documents, load_documents
from .handler import handler, warmup
from .llm_provider import get_embeddings, get_settings
from .vector_store import build_vector_store, persist_vector_store


def _str_to_bool(value: str) -> bool:
    return value.lower() in {"1", "true", "t", "yes", "y"}


def _bootstrap_vector_store() -> None:
    settings = get_settings()
    target_dir = Path(settings.vector_store_path)

    if target_dir.exists():
        return

    # Sempre constrói o vector store automaticamente se não existir

    data_dir = Path(settings.rag_data_path)
    documents = load_documents(data_dir)
    if not documents:
        raise ValueError(
            f"Nenhum documento suportado encontrado em '{data_dir}'. Adicione arquivos .txt."
        )

    chunks = chunk_documents(documents)
    embeddings = get_embeddings()
    store = build_vector_store(chunks, embeddings)
    persist_vector_store(store, target_dir)


def _dispatch_handler(event: Dict[str, Any]) -> JSONResponse:
    response = handler(event)
    status_code = response.get("statusCode", 500)
    headers = response.get("headers") or {}

    raw_body = response.get("body", "{}")
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        payload = {"raw": raw_body}

    header_map = {str(key): str(value) for key, value in headers.items()}
    return JSONResponse(payload, status_code=status_code, headers=header_map or None)


app = FastAPI(title="AI Agent API", version="0.1.0")


@app.on_event("startup")
def _on_startup() -> None:
    try:
        _bootstrap_vector_store()
        warmup()
    except FileNotFoundError as exc:  # pragma: no cover - configuração incorreta
        message = (
            "Vector store ausente e AUTO_BUILD_VECTOR_STORE desativado. "
            "Execute 'python vetorize.py' ou defina AUTO_BUILD_VECTOR_STORE=true."
        )
        raise RuntimeError(message) from exc


@app.get("/")
def read_root() -> Dict[str, Any]:
    return {
        "message": "Use POST /query com JSON {'question': '...'} ou GET /health",
        "endpoints": {"health": "/health", "query": "/query"},
    }


@app.get("/health")
def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/query")
def query_get(question: str = Query(..., min_length=1)) -> JSONResponse:
    event = {
        "question": question,
        "httpMethod": "GET",
        "path": "/query",
        "queryStringParameters": {"question": question},
    }
    return _dispatch_handler(event)


@app.post("/query")
async def query_post(request: Request) -> JSONResponse:
    raw_body = await request.body()
    body_text = raw_body.decode("utf-8") if raw_body else ""

    if body_text:
        try:
            payload = json.loads(body_text)
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail="JSON inválido no corpo da requisição.") from exc
    else:
        payload = {}

    question = payload.get("question") or payload.get("query") or request.query_params.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Informe 'question' no corpo ou na query string.")

    event: Dict[str, Any] = {
        "question": question,
        "body": body_text,
        "headers": dict(request.headers),
        "httpMethod": "POST",
        "path": request.url.path,
    }

    if request.query_params:
        event["queryStringParameters"] = dict(request.query_params)

    return _dispatch_handler(event)


def run() -> None:
    import uvicorn  # type: ignore[import]

    host = os.getenv("AGENT_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("AGENT_SERVER_PORT", "8000"))
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=_str_to_bool(os.getenv("UVICORN_RELOAD", "false")),
    )


if __name__ == "__main__":
    run()
