# pipeline.py
from .data_loading import FileLoader
from .text_processing import TextExtractorCleaner
from .embeddings import EmbeddingEngine
from .vector_store import CreateVectorStore
from .dimensionality import DimensionalityReduction
from .clustering import Clustering
from .visualization import UMAPVisualization
from .summarization import OpenAISummarizer

pdf_files = list(file_path.glob("*.pdf"))

files_loades = FileLoader(pdf_files).load_files()
extracted_texts = TextExtractorCleaner(files_loades).clean_texts()
embedded_texts = EmbeddingEngine(extracted_texts).create_embeddings()
vector_store = CreateVectorStore(embedded_texts).create_vector_store()

reduced_vectorstore = DimensionalityReduction(vector_store, metric='cosine', n_neighbors=10, min_dist=0.1).umap()
clustered_vectors = Clustering(reduced_vectorstore, min_cluster_size=5).hdbscan()
#UMAP_visualization(clustered_vectors).visualize_umap()

df_summary = ClusterSummary(clustered_vectors, vector_store).get_dataframe()

df_summary.to_csv("temp_data.csv", index=False)
