
import logging
from .data_loading import DocumentData  # Względny import
import spacy
from spacy_cleaner import Cleaner, processing
logger = logging.getLogger(__name__)

import spacy
from spacy_cleaner import Cleaner, processing


class TextExtractorCleaner:
    def __init__(self, texts: list[DocumentData]) -> None:
        self.texts = texts
        logger.info("Loading spaCy model...")
        self.nlp = spacy.load("en_core_web_sm")

        logger.info("Initializing text cleaner...")
        self.cleaner = Cleaner(
            self.nlp,
            processing.remove_stopword_token,
            processing.remove_punctuation_token,
            processing.mutate_lemma_token,
        )

    def _clean_single_text(self, single_text: str) -> str:
        try:
            cleaned_result = self.cleaner.clean([single_text])

            if isinstance(cleaned_result, list) and len(cleaned_result) > 0:
                cleaned_text = cleaned_result[0]

                if isinstance(cleaned_text, str):
                    return " ".join(cleaned_text.split()) 
                elif isinstance(cleaned_text, list):
                    return " ".join(cleaned_text)

            return None

        except Exception as e:
            logger.info(f"Failed to clean {single_text}: {e}")
            return None

    def clean_texts(self) -> list[DocumentData]:
        logger.info(f"Starting text cleaning for {len(self.texts)} documents...")

        for doc_data in self.texts:
            # Batch processing
            page_texts = [doc.page_content for doc in doc_data.content if doc.page_content.strip()]

            if page_texts:
                try:
                    cleaned_results = self.cleaner.clean(page_texts)

                    processed_pages = []
                    for cleaned_text in cleaned_results:
                        if isinstance(cleaned_text, str):
                            processed_pages.append(" ".join(cleaned_text.split()))
                        elif isinstance(cleaned_text, list):
                            processed_pages.append(" ".join(cleaned_text))

                    doc_data.cleaned_text = " ".join(filter(None, processed_pages))

                except Exception as e:
                    logger.warning(f"Batch processing failed for {doc_data.filename}: {e}")

                    all_pages_text = []
                    for document in doc_data.content:
                        cleaned = self._clean_single_text(document.page_content)
                        if cleaned:
                            all_pages_text.append(cleaned)
                    doc_data.cleaned_text = " ".join(all_pages_text)
            else:
                doc_data.cleaned_text = ""

        logger.info(f"{len(self.texts)} texts cleaned successfully")
        return self.texts
