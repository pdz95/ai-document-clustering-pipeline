# src/s3_organizer.py
import zipfile
import tempfile
from pathlib import Path


class S3FileOrganizer:
    def __init__(self, s3_handler, bucket_name):
        self.s3_handler = s3_handler
        self.bucket_name = bucket_name

    def organize_files_by_clusters(self, df_summary, session_id):
        """Copy files from uploads/ to organized/cluster_folders/"""
        organized_paths = []

        for cluster_id in df_summary['HDBCLUSTER'].unique():
            cluster_data = df_summary[df_summary['HDBCLUSTER'] == cluster_id]
            cluster_title = cluster_data['cluster_title'].iloc[0]
            clean_title = cluster_title.replace(' ', '_')

            for _, row in cluster_data.iterrows():
                filename = row['filename']
                source_key = f"sessions/{session_id}/uploads/{filename}"
                dest_key = f"sessions/{session_id}/organized/Cluster_{cluster_id}_{clean_title}/{filename}"

                # Copy in S3
                copy_source = {'Bucket': self.bucket_name, 'Key': source_key}
                self.s3_handler.s3_client.copy_object(
                    CopySource=copy_source,
                    Bucket=self.bucket_name,
                    Key=dest_key
                )
                organized_paths.append(dest_key)

        return organized_paths

    def create_zip_from_organized(self, organized_paths, session_id):
        """Create ZIP with all clusters from organized S3 paths"""
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / f"organized_docs_{session_id}.zip"

            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for s3_key in organized_paths:
                    # Extract: Cluster_X_Title/file.pdf from full S3 path
                    relative_path = '/'.join(s3_key.split('/')[3:])
                    temp_file = Path(temp_dir) / Path(s3_key).name

                    self.s3_handler.download_file(s3_key, temp_file)
                    zipf.write(temp_file, relative_path)

            return zip_path.read_bytes(), zip_path.name