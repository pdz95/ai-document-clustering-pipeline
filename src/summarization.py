import os
from openai import OpenAI
import pandas as pd
from .data_loading import DocumentData

class OpenAISummarizer:
    def __init__(self,  combined_texts : str) -> None:
        self.combined_texts = combined_texts
    def _open_AI_API(self, ):
        import os
        from openai import OpenAI

        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        response = client.responses.create(
            model="gpt-4.1-nano",
            instructions="""Analyze the following collection of academic documents that have been grouped together by similarity clustering.

            Return your response as valid JSON in this exact format:
            {
                "title": "descriptive title (5-10 words maximum) of all documents",
                "summary": "Maximum 2-3 sentence overview of main themes and topics. It must be very concise",
            }

            Make sure to return ONLY valid JSON, nothing else.""",
            input=self.combined_texts,
        )

        import json
        return json.loads(response.output_text)

class ClusterSummary:
    def __init__(self, clustered_vectors, vector_store):
        self.clustered_vectors = clustered_vectors
        self.vector_store = vector_store

    def _analyze_single_cluster(self, cluster_id, all_docs, max_chars_per_doc=5000):
        """Ukryta metoda do analizy pojedynczego klastra"""
        all_metadata = self.vector_store.get(include=['metadatas'])

        cluster_mask = self.clustered_vectors['HDBCLUSTER'] == cluster_id
        cluster_indices = self.clustered_vectors[cluster_mask].index.tolist()

        # Pobierz dokumenty z ograniczeniem znaków
        truncated_docs = [all_docs['documents'][i][:max_chars_per_doc] for i in cluster_indices]
        combined_text = " ".join(truncated_docs)

        ai_result = OpenAISummarizer(combined_text)._open_AI_API()

        # Dodaj AI wyniki do danych klastra
        cluster_data = self.clustered_vectors[cluster_mask].copy()
        cluster_data['filename'] = [all_metadata['metadatas'][i]['filename'] for i in cluster_indices]
        cluster_data['cluster_title'] = ai_result['title']
        cluster_data['cluster_summary'] = ai_result['summary']

        return cluster_data

    def get_dataframe(self):
        """Tworzy DataFrame z analizą wszystkich klastrów"""
        all_docs = self.vector_store.get(include=['documents'])
        results = []

        for cluster_id in self.clustered_vectors['HDBCLUSTER'].unique():
            if cluster_id == -1:  # pomiń noise
                continue

            print(f"Przetwarzam klaster {cluster_id}...")
            cluster_data = self._analyze_single_cluster(cluster_id, all_docs)
            results.append(cluster_data)

        return pd.concat(results, ignore_index=True)
