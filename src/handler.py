"""Primary RAG handler supporting multiple deployment targets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional, cast

from langchain.chains import RetrievalQA

from .data_loader import chunk_documents, load_documents
from .llm_provider import get_embeddings, get_llm, get_settings
from .prompts import get_qa_prompt
from .vector_store import load_vector_store

_QA_CHAIN: Optional[RetrievalQA] = None


def _build_chain() -> RetrievalQA:
    settings = get_settings()
    embeddings = get_embeddings()
    store = load_vector_store(Path(settings.vector_store_path), embeddings)
    retriever = store.as_retriever(search_kwargs={"k": settings.rag_top_k})

    return RetrievalQA.from_chain_type(
        llm=get_llm(),
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": get_qa_prompt()},
        return_source_documents=True,
    )


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Serverless-friendly entrypoint wrapping the RAG pipeline."""

    global _QA_CHAIN
    if _QA_CHAIN is None:
        try:
            _initialize_chain()
        except FileNotFoundError as exc:
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {
                        "error": "Vector store não encontrado. Execute 'python vetorize.py'.",
                        "details": str(exc),
                    }
                ),
            }

    question = _extract_question(event)
    if not question:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Informe a pergunta no campo 'question'."}),
        }

    chain = cast(RetrievalQA, _QA_CHAIN)
    response = chain.invoke({"query": question})
    sources = [
        {
            "source": doc.metadata.get("source"),
            "preview": doc.page_content[:240],
        }
        for doc in response.get("source_documents", [])
    ]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "answer": response.get("result", ""),
                "sources": sources,
            },
            ensure_ascii=False,
        ),
    }


def _initialize_chain() -> None:
    global _QA_CHAIN
    _QA_CHAIN = _build_chain()


def _extract_question(event: Dict[str, Any]) -> Optional[str]:
    if "question" in event:
        return event["question"]

    if "body" in event:
        body = event["body"]
        if isinstance(body, str):
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                return body
        elif isinstance(body, dict):
            payload = body
        else:
            payload = {}
        return payload.get("question") or payload.get("query")

    if "queryStringParameters" in event and isinstance(event["queryStringParameters"], dict):
        params = event["queryStringParameters"]
        return params.get("question") or params.get("query")

    return None


def warmup() -> None:
    """Cria a cadeia antecipadamente para cold start mais rápido."""

    if _QA_CHAIN is None:
        _initialize_chain()


if __name__ == "__main__":
    try:
        warmup()
    except FileNotFoundError as exc:
        print(
            "Vector store não encontrado. Execute 'python vetorize.py' antes de testar o handler."
        )
        raise SystemExit(str(exc))

    pergunta = input("Pergunta para o agente: ")
    resultado = handler({"question": pergunta})
    corpo = json.loads(resultado["body"])
    if "error" in corpo:
        print("\nErro:", corpo["error"])
        if corpo.get("details"):
            print("Detalhes:", corpo["details"])
    else:
        print("\nResposta:\n", corpo.get("answer"))
        if corpo.get("sources"):
            print("\nFontes:")
            for item in corpo["sources"]:
                print(f"- {item['source']}")
