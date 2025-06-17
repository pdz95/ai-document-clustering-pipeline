import streamlit as st
import pandas as pd
import os
import sys
import json
from pathlib import Path

import plotly.express as px
import boto3

from deployment.ui.sidebar import create_sidebar
from deployment.core.session_manager import SessionManager
from deployment.core.s3_handler import S3Handler
from deployment.core.s3_organizer import S3FileOrganizer

if sys.platform.startswith('linux'):
    import asyncio

    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except:
        pass

# Page configuration
st.set_page_config(
    page_title="Document Clustering App",
    page_icon="📄",
    layout="wide"
)

# Initialize global components
lambda_client = boto3.client('lambda', region_name='us-east-1')
S3_BUCKET = os.environ.get('S3_BUCKET_NAME_PDF', 'your-pdf-clustering-bucket')
s3_handler = S3Handler(S3_BUCKET)


def call_lambda_embedding(s3_keys_list):
    """Call Lambda function with S3 file paths"""
    full_s3_paths = [f"s3://{S3_BUCKET}/{key}" for key in s3_keys_list]

    payload = {"s3_files": full_s3_paths}

    response = lambda_client.invoke(
        FunctionName='document-clustering-api',
        Payload=json.dumps(payload)
    )

    payload_result = response['Payload'].read()
    return json.loads(payload_result)


def parse_lambda_response(lambda_result):
    """Convert Lambda clustering result to DataFrame"""
    if lambda_result.get('statusCode') != 200:
        st.error(f"Lambda failed with status: {lambda_result.get('statusCode')}")
        return pd.DataFrame()

    body_data = json.loads(lambda_result['body'])

    if 'error' in body_data:
        st.error(f"Lambda error: {body_data['error']}")
        return pd.DataFrame()

    clusters_data = body_data['clusters']
    rows = []

    for cluster in clusters_data:
        cluster_id = cluster['cluster_id']
        title = cluster['title']
        summary = cluster['summary']
        files = cluster['files']
        umap1_coords = cluster['coordinates']['umap1']
        umap2_coords = cluster['coordinates']['umap2']

        for i, filename in enumerate(files):
            rows.append({
                'filename': filename,
                'HDBCLUSTER': cluster_id,
                'cluster_title': title,
                'cluster_summary': summary,
                'UMAP1': umap1_coords[i],
                'UMAP2': umap2_coords[i]
            })

    return pd.DataFrame(rows)


def handle_file_upload_and_processing(uploaded_files):
    """Handle the complete upload and processing workflow"""
    with st.spinner("Uploading to S3..."):
        session_id = SessionManager.get_or_create_session_id()
        st.info(f"Session: {session_id}")

        temp_folder = Path("temp_pdfs")
        temp_folder.mkdir(exist_ok=True)

        s3_keys = []
        for uploaded_file in uploaded_files:
            file_path = temp_folder / uploaded_file.name
            file_content = uploaded_file.read()
            file_path.write_bytes(file_content)

            s3_key = SessionManager.get_s3_upload_path(uploaded_file.name)
            uploaded_file.seek(0)

            if s3_handler.upload_file(uploaded_file.read(), s3_key):
                s3_keys.append(s3_key)
            else:
                st.error(f"Failed to upload {uploaded_file.name} to S3")

        st.session_state.s3_keys = s3_keys
        st.success(f"Uploaded {len(s3_keys)} files to S3")

    with st.spinner("Processing with Lambda..."):
        lambda_result = call_lambda_embedding(s3_keys)
        df_summary = parse_lambda_response(lambda_result)
        st.session_state.df_summary = df_summary
        st.success("Processing complete!")


# Main App
st.title("📄 AI-Powered Document Organization")
create_sidebar()

st.info("""
This tool automatically analyzes and clusters your PDF documents by content similarity. 
Upload 10+ PDFs, and our machine learning pipeline will group them into thematic clusters with AI-generated titles and summaries. 
Perfect for researchers, analysts, and anyone working with large document collections.

⚠️ **IMPORTANT DISCLAIMER:** This system is for educational and demonstration purposes only. Due to privacy concerns, please do not upload any private data!
""")

tab1, tab2 = st.tabs(["## 📤 Upload & Cluster", "## 📋 About the project"])

with tab1:
    col1, col2, col3 = st.columns([2, 2, 3])

    with col1:
        st.subheader("Upload PDF files here")
        uploaded_files = st.file_uploader(
            "Upload PDF files (max 60)",
            type="pdf",
            accept_multiple_files=True
        )

        if uploaded_files and len(uploaded_files) > 60:
            st.error("Too many files! Please upload maximum 60 PDFs.")
            uploaded_files = None
        if uploaded_files and len(uploaded_files) < 10:
            st.error("Please upload minimum 10 PDFs.")
            uploaded_files = None

        if uploaded_files:
            st.success(f"Uploaded {len(uploaded_files)} files")

            if st.button("Process Documents"):
                handle_file_upload_and_processing(uploaded_files)
        else:
            st.info("Please upload PDF files to get started")

    with col2:
        st.subheader("Document Clusters")

        if 'df_summary' in st.session_state and not st.session_state.df_summary.empty:
            fig = px.scatter(
                st.session_state.df_summary,
                x='UMAP1',
                y='UMAP2',
                color='HDBCLUSTER',
                hover_data=['filename', 'cluster_title'],
                title='Document Clusters'
            )

            fig.update_layout(
                width=500,
                height=500,
                margin=dict(l=0, r=0, t=30, b=0),
            )

            st.plotly_chart(fig, use_container_width=True)
            st.write(f"Found {st.session_state.df_summary['HDBCLUSTER'].nunique()} clusters")
            st.write(f"{len(st.session_state.df_summary)} documents processed")

            if st.button("📁 Organize PDFs by Clusters"):
                with st.spinner("Organizing files and creating ZIP..."):
                    organizer = S3FileOrganizer(s3_handler, S3_BUCKET)
                    session_id = SessionManager.get_or_create_session_id()

                    organized_paths = organizer.organize_files_by_clusters(
                        st.session_state.df_summary, session_id
                    )

                    zip_data, zip_name = organizer.create_zip_from_organized(
                        organized_paths, session_id
                    )

                    st.download_button("📥 Download Organized ZIP", zip_data, zip_name, "application/zip")
                    st.success("✅ Files organized and ready for download!")
        else:
            st.info("Upload and process documents to see clusters")

    with col3:
        st.subheader("Cluster Summary")

        if 'df_summary' in st.session_state and not st.session_state.df_summary.empty:
            for cluster_id in st.session_state.df_summary['HDBCLUSTER'].unique():
                cluster_data = st.session_state.df_summary[st.session_state.df_summary['HDBCLUSTER'] == cluster_id]

                title = cluster_data['cluster_title'].iloc[0]
                summary = cluster_data['cluster_summary'].iloc[0]
                file_count = len(cluster_data)

                st.write(f"**Cluster {cluster_id}**: {title}")
                st.write(f"Summary: {summary}")
                st.write(f"File count: {file_count}")
                st.write("---")
        else:
            st.info("Upload and process documents to see summary")

with tab2:
    st.header("About the project")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.info("""
        **🔧 Technical Architecture**

        Complete serverless ML pipeline for document analysis:

        • **Frontend:** Streamlit + Plotly interactive charts

        • **Backend:** Python 3.11 + pandas + numpy

        • **ML Pipeline:** SentenceTransformers + UMAP + HDBSCAN

        • **Cloud:** AWS Lambda + ECR + S3 + EC2

        • **Infrastructure:** Ubuntu 24.04 + systemd

        • **AI Integration:** OpenAI GPT-4 for summarization

        • **Document Processing:** PyMuPDF + LangChain + spaCy

        • **Vector Database:** ChromaDB for embeddings

        • **Session Management:** Temporary S3 storage

        • **Download System:** ZIP creation with organized folders
        """)

    with col2:
        st.info("""
        **📚 For Researchers & Analysts**

        **The Challenge:**

        • Large document collections are overwhelming

        • Manual organization is time-consuming

        • Similar documents scattered across folders

        • No easy way to discover themes

        **The Solution:**

        • AI-powered semantic analysis

        • Automatic thematic clustering

        • Smart folder organization

        • Interactive visualization of document relationships

        **Perfect for:**

        • Academic research paper organization

        • Legal document classification

        • Business report analysis

        • Knowledge management systems

        • Literature review preparation
        """)

    with col3:
        st.info("""
        **🚀 Future Enhancements**

        • **Multiple file formats** (Word, PowerPoint, Excel)

        • **Advanced clustering** - hierarchical and custom parameters

        • **Custom models** - domain-specific embeddings

        • **Search functionality** - semantic document search

        • **Export options** - CSV, JSON metadata

        """)