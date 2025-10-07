import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    llm_provider: Literal["google", "placeholder"]
    google_api_key: str
    google_llm_model: str
    google_embedding_model: str
    rag_data_path: str
    vector_store_path: str
    rag_top_k: int


def _load_env_settings() -> Settings:
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "google").lower()
    google_key = os.getenv("GOOGLE_API_KEY", "")
    if provider == "google" and not google_key:
        raise EnvironmentError(
            "Defina GOOGLE_API_KEY no arquivo .env para utilizar o provedor Google."
        )

    return Settings(
        llm_provider=provider,  # type: ignore[arg-type]
        google_api_key=google_key,
    google_llm_model=os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash"),
        google_embedding_model=os.getenv(
            "GOOGLE_EMBEDDING_MODEL", "models/text-embedding-004"
        ),
        rag_data_path=os.getenv("RAG_DATA_PATH", "rag_data"),
        vector_store_path=os.getenv("VECTOR_STORE_PATH", "vector_store"),
        rag_top_k=int(os.getenv("RAG_TOP_K", "5")),
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return _load_env_settings()


@lru_cache(maxsize=1)
def get_embeddings():
    settings = get_settings()

    if settings.llm_provider == "google":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings(
            model=settings.google_embedding_model,
            google_api_key=settings.google_api_key,
        )

    raise NotImplementedError(
        "Somente o provedor Google está configurado neste template inicial."
    )


@lru_cache(maxsize=1)
def get_llm():
    settings = get_settings()

    if settings.llm_provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=settings.google_llm_model,
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
            google_api_key=settings.google_api_key,
        )

    raise NotImplementedError(
        "Somente o provedor Google está configurado neste template inicial."
    )
