import numpy as np
from sentence_transformers import SentenceTransformer
import logging
from .data_loading import DocumentData

logger = logging.getLogger(__name__)

class EmbeddingEngine:
    def __init__(self, text_list: list[DocumentData]) -> None:
        self.embedding_model = SentenceTransformer("malteos/scincl")
        self.texts = text_list

    def _embedding(self, text_embedding: str) -> np.ndarray | None:
        try:
            if not text_embedding:
                logger.info("An error ocured while embedding")
                return None

            embedding = self.embedding_model.encode(text_embedding)
            return embedding

        except Exception as e:
            logger.info(f"Failed to embed {text_embedding}: {e}")
            return None

    def create_embeddings(self) -> list[DocumentData]:
        for doc_data in self.texts:
            embedded_doc = self._embedding(doc_data.cleaned_text)
            doc_data.embedding = embedded_doc

        logger.info(f"{len(self.texts)} texts embedded")

        return self.texts