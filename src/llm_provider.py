"""Provider padrão focado no suporte ao Google Generative AI."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    llm_provider: Literal["google", "placeholder"]
    temperature: float
    rag_data_path: str
    vector_store_path: str
    rag_top_k: int
    google_api_key: str
    google_llm_model: str
    google_embedding_model: str


def _load_env_settings() -> Settings:
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "google").lower()
    if provider != "google":
        raise NotImplementedError(
            "Este template padrão suporta apenas o provedor Google. Consulte ops/providers para alternativas."
        )

    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        raise EnvironmentError("Defina GOOGLE_API_KEY no arquivo .env para utilizar o provedor Google.")

    return Settings(
        llm_provider=provider,  # type: ignore[arg-type]
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
        rag_data_path=os.getenv("RAG_DATA_PATH", "rag_data"),
        vector_store_path=os.getenv("VECTOR_STORE_PATH", "vector_store"),
        rag_top_k=int(os.getenv("RAG_TOP_K", "5")),
        google_api_key=api_key,
        google_llm_model=os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash"),
        google_embedding_model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/text-embedding-004"),
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return _load_env_settings()


@lru_cache(maxsize=1)
def get_embeddings():
    settings = get_settings()
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)
    return GoogleGenerativeAIEmbeddings(
        model=settings.google_embedding_model,
    )


@lru_cache(maxsize=1)
def get_llm():
    settings = get_settings()
    from langchain_google_genai import ChatGoogleGenerativeAI

    os.environ.setdefault("GOOGLE_API_KEY", settings.google_api_key)
    return ChatGoogleGenerativeAI(
        model=settings.google_llm_model,
        temperature=settings.temperature,
    )


__all__ = ["Settings", "get_settings", "get_embeddings", "get_llm"]