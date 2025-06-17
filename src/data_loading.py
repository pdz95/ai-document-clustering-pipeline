from dataclasses import dataclass
from pathlib import Path
import numpy as np
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)

@dataclass
class DocumentData:
    filename: str
    content: list[Document]
    page_count: int
    cleaned_text: str | None = None
    embedding: np.ndarray | None = None

class FileLoader:
    def __init__(self, files: list[Path]) -> None:
        self.files_loaded =  [Path(f) if isinstance(f, str) else f for f in files]
        self.loaded_documents: list[DocumentData] = []

    def _load_single_file(self, file_path: Path) -> DocumentData | None:
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File {file_path} not found")

            loader = PyMuPDFLoader(str(file_path))
            data = loader.load()

            return DocumentData(
                filename=file_path.name,
                content=data,
                page_count=len(data)
            )

        except Exception as e:
            print(f"Failed to load {file_path}: {e}")
            return None

    def load_files(self) -> list[DocumentData]:
        self.loaded_documents.clear()

        for file_path in self.files_loaded:
            doc = self._load_single_file(file_path)
            if doc:
                self.loaded_documents.append(doc)

        logger.info(f"Successfully loaded {len(self.loaded_documents)} out of {len(self.files_loaded)} files")
        return self.loaded_documents