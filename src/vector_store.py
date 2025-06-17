import chromadb
import logging
from .data_loading import DocumentData

logger = logging.getLogger(__name__)


class CreateVectorStore:
    def __init__(self, document_db: list[DocumentData]) -> None:
        self.raw_data = document_db
        self.client = chromadb.Client()
        self.collection = None
        self.database = []

    def _save_to_vector_store(self) -> None:
        for doc_data in self.raw_data:
            # Sprawdź czy embedding istnieje
            if doc_data.embedding is None:
                logger.warning(f"Skipping {doc_data.filename} - no embedding")
                continue

            self.collection.add(
                embeddings=doc_data.embedding.tolist(),
                documents=doc_data.cleaned_text,
                ids=doc_data.filename.replace('.pdf', ''),
                metadatas={
                    "filename": doc_data.filename,
                    "total_pages": doc_data.page_count,
                    "doc_type": "full_document"
                }
            )

    def create_vector_store(self) -> chromadb.api.models.Collection.Collection:
        collection_name = "papers"

        # Sprawdź czy kolekcja istnieje i usuń ją
        try:
            existing_collections = self.client.list_collections()
            collection_exists = any(col.name == collection_name for col in existing_collections)

            if collection_exists:
                self.client.delete_collection(collection_name)
                print(f"Usunięto istniejącą kolekcję: {collection_name}")
        except Exception as e:
            print(f"Błąd podczas sprawdzania/usuwania kolekcji: {e}")

        # Utwórz nową kolekcję
        self.collection = self.client.create_collection(collection_name)
        self._save_to_vector_store()
        return self.collection