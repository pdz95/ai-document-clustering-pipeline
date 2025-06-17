import logging
from .data_loading import DocumentData

logger = logging.getLogger(__name__)


class TextExtractorCleaner:
    def __init__(self, texts: list[DocumentData]) -> None:
        self.texts = texts

    def clean_texts(self) -> list[DocumentData]:
        for doc_data in self.texts:
            # Połącz wszystkie strony w jeden tekst
            all_text = " ".join([doc.page_content for doc in doc_data.content])
            doc_data.cleaned_text = all_text.strip()

        return self.texts