from pathlib import Path
from typing import Iterable, List

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_documents(data_dir: Path) -> List[Document]:
    """Carrega os arquivos suportados da pasta de RAG."""
    supported_suffixes = {".txt", ".md"}
    documents: List[Document] = []

    if not data_dir.exists():
        raise FileNotFoundError(
            f"Diretório de dados '{data_dir}' não encontrado. Crie-o e adicione documentos."
        )

    for file_path in data_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in supported_suffixes:
            text = file_path.read_text(encoding="utf-8")
            documents.append(
                Document(page_content=text, metadata={"source": file_path.name})
            )

    if not documents:
        raise ValueError(
            f"Nenhum documento suportado encontrado em '{data_dir}'. Adicione arquivos .txt ou .md."
        )

    return documents


def chunk_documents(
    documents: Iterable[Document],
    *,
    chunk_size: int = 750,
    chunk_overlap: int = 120,
) -> List[Document]:
    """Divide os documentos em chunks semânticos."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". "],
    )
    return splitter.split_documents(list(documents))
