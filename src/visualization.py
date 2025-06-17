import pandas as pd
import seaborn as sns

class UMAPVisualization:
    def __init__(self, reducted_results: pd.DataFrame) -> None:
        self.reducted_results = reducted_results

    def visualize_umap(self) -> None:
        sns.set_theme(style="white")
        plt.figure(figsize=(8, 8))
        sns.scatterplot(x="UMAP1", y="UMAP2", hue="HDBCLUSTER", palette="pastel", data=self.reducted_results)
        plt.title("Document Clusters in UMAP Space")
        plt.show()