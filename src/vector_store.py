from pathlib import Path
from typing import Iterable

from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS


def build_vector_store(documents: Iterable[Document], embeddings) -> FAISS:
    """Cria um vetor FAISS a partir dos documentos chunkados."""
    return FAISS.from_documents(list(documents), embeddings)


def persist_vector_store(store: FAISS, target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    store.save_local(str(target_dir))


def load_vector_store(target_dir: Path, embeddings) -> FAISS:
    if not target_dir.exists():
        raise FileNotFoundError(
            f"Vector store não encontrado em '{target_dir}'. Execute 'python vetorize.py'."
        )

    return FAISS.load_local(
        str(target_dir),
        embeddings,
        allow_dangerous_deserialization=True,
    )
