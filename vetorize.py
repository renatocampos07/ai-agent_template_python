from pathlib import Path

from src.data_loader import chunk_documents, load_documents
from src.llm_provider import get_embeddings, get_settings
from src.vector_store import build_vector_store, persist_vector_store


def main() -> None:
	settings = get_settings()
	data_dir = Path(settings.rag_data_path)
	target_dir = Path(settings.vector_store_path)

	documents = load_documents(data_dir)
	chunks = chunk_documents(documents)

	embeddings = get_embeddings()
	store = build_vector_store(chunks, embeddings)
	persist_vector_store(store, target_dir)

	print(
		f"Vector store criado em '{target_dir}'. Total de chunks: {len(chunks)}."
	)


if __name__ == "__main__":
	main()
