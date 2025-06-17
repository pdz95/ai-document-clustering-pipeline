# deployment.core/s3_handler.py
import boto3
import os
from botocore.exceptions import ClientError
import streamlit as st
from pathlib import Path


class S3Handler:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
        )

    def upload_file(self, file_content, s3_key):
        """Upload file content to S3"""
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content
            )
            return True
        except ClientError as e:
            st.error(f"Failed to upload {s3_key}: {e}")
            return False

    def upload_local_file(self, local_path, s3_key):
        """Upload local file to S3"""
        try:
            self.s3_client.upload_file(str(local_path), self.bucket_name, s3_key)
            return True
        except ClientError as e:
            st.error(f"Failed to upload {local_path}: {e}")
            return False

    def download_file(self, s3_key, local_path):
        """Download file from S3 to local path"""
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, str(local_path))
            return True
        except ClientError as e:
            st.error(f"Failed to download {s3_key}: {e}")
            return False