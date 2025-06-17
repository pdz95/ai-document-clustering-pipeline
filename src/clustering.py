import pandas as pd
import umap
from sklearn.cluster import HDBSCAN
import logging

logger = logging.getLogger(__name__)
class Clustering:
    def __init__(self, reducted_results: pd.DataFrame, min_cluster_size=10) -> None:
        self.reducted_results = reducted_results
        self.clustering_algo = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=3)
        self.clustering_results = None

    def hdbscan(self) -> pd.DataFrame:
        fitted_model = self.clustering_algo.fit(self.reducted_results)
        self.clustering_results = self.reducted_results.copy()
        self.clustering_results["HDBCLUSTER"] = fitted_model.labels_
        logger.info("HDB clustering reduction done.")
        return self.clustering_results