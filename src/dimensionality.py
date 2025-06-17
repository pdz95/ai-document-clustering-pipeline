import pandas as pd
import logging
import umap
logger = logging.getLogger(__name__)
class DimensionalityReduction:
    def __init__(self, vector_store, metric='cosine', n_neighbors=15, min_dist=0.1) -> None:
        self.vector_store = vector_store
        self.reducer = umap.UMAP(metric=metric, n_neighbors=n_neighbors, min_dist=min_dist, random_state=1)
        self.results = []

    def umap(self) -> pd.DataFrame:
        results = self.vector_store.get(include=['embeddings'])
        embedding = results['embeddings']
        embedding_umap = self.reducer.fit_transform(embedding)
        self.results = pd.DataFrame(embedding_umap, columns=["UMAP1", "UMAP2"])
        logger.info("UMAP dimensionality reduction done.")
        return self.results