import json
import boto3
import os
from pathlib import Path

import sys

os.environ['NUMBA_CACHE_DIR'] = '/tmp'
os.environ['NUMBA_DISABLE_JIT'] = '1'
os.environ['TRANSFORMERS_CACHE'] = '/tmp'
os.environ['HF_HOME'] = '/tmp'
os.environ['SENTENCE_TRANSFORMERS_HOME'] = '/tmp'
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


# Import your modules directly - no need for complex path manipulation
from src.data_loading import FileLoader
from src.text_processing import TextExtractorCleaner
from src.embeddings import EmbeddingEngine
from src.vector_store import CreateVectorStore
from src.dimensionality import DimensionalityReduction
from src.clustering import Clustering
from src.summarization import ClusterSummary


def lambda_handler(event, context):
    """
    AWS Lambda handler for document clustering API
    """
    try:
        # Parse input
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', event)

        s3_files = body.get('s3_files', [])
        parameters = body.get('parameters', {})

        # Validate input
        if not s3_files:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'No files provided'})
            }

        # Download files from S3 to /tmp
        s3_client = boto3.client('s3')
        local_files = []

        for s3_path in s3_files:
            # Parse s3://bucket/key format
            if s3_path.startswith('s3://'):
                s3_path = s3_path[5:]

            bucket, key = s3_path.split('/', 1)
            local_path = f"/tmp/{Path(key).name}"

            s3_client.download_file(bucket, key, local_path)
            local_files.append(Path(local_path))

        # Run your processing pipeline
        files_loaded = FileLoader(local_files).load_files()
        extracted_texts = TextExtractorCleaner(files_loaded).clean_texts()
        embedded_texts = EmbeddingEngine(extracted_texts).create_embeddings()
        vector_store = CreateVectorStore(embedded_texts).create_vector_store()

        # Apply parameters
        n_neighbors = parameters.get('n_neighbors', 10)
        min_dist = parameters.get('min_dist', 0.1)
        min_cluster_size = parameters.get('min_cluster_size', 3)

        reduced_vectorstore = DimensionalityReduction(
            vector_store,
            metric='cosine',
            n_neighbors=n_neighbors,
            min_dist=min_dist
        ).umap()

        clustered_vectors = Clustering(
            reduced_vectorstore,
            min_cluster_size=min_cluster_size
        ).hdbscan()

        df_summary = ClusterSummary(clustered_vectors, vector_store).get_dataframe()

        # Format response
        clusters = []
        for cluster_id in df_summary['HDBCLUSTER'].unique():
            cluster_data = df_summary[df_summary['HDBCLUSTER'] == cluster_id]

            clusters.append({
                'cluster_id': int(cluster_id),
                'title': cluster_data['cluster_title'].iloc[0] if len(cluster_data) > 0 else '',
                'summary': cluster_data['cluster_summary'].iloc[0] if len(cluster_data) > 0 else '',
                'files': cluster_data['filename'].tolist(),
                'coordinates': {
                    'umap1': cluster_data['UMAP1'].tolist(),
                    'umap2': cluster_data['UMAP2'].tolist()
                },
                'document_count': len(cluster_data)
            })

        # Clean up temp files
        for file_path in local_files:
            if file_path.exists():
                file_path.unlink()

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'clusters': clusters,
                'total_documents': len(df_summary),
                'total_clusters': len(clusters),
                'parameters_used': parameters
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }