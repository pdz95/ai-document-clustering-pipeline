# AI-Powered Document Clustering Pipeline

Intelligent PDF organization system using machine learning-powered semantic clustering and automated content analysis.

## Live Demo
🚀 **[View Live Application](http://3.94.54.203:8082)**

This production system is deployed on AWS cloud infrastructure. 

## Key Features

- **Semantic clustering** - Groups documents by content similarity using SentenceTransformers
- **AI-generated summaries** - OpenAI GPT-4 creates cluster titles and descriptions  
- **Interactive visualization** - UMAP 2D scatter plots of document relationships
- **Automated organization** - Downloads clustered PDFs in organized ZIP folders
- **Serverless architecture** - AWS Lambda + Streamlit for scalable processing
- **Real-time processing** - Upload 10-60 PDFs and get instant clustering results

## Architecture
├── Frontend (Streamlit + Plotly visualization)
├── Backend (AWS Lambda + ECR containers)
├── ML Pipeline (SentenceTransformers + UMAP + HDBSCAN)
├── Vector Storage (ChromaDB embeddings)
├── AI Integration (OpenAI GPT-4 summarization)
└── Infrastructure (AWS S3 + EC2 + Ubuntu + systemd)

### How It Works

Document upload - Upload 10-60 PDF files via Streamlit interface
Text extraction - PyMuPDF extracts clean text from documents
Embedding generation - SentenceTransformers creates semantic vectors
Dimensionality reduction - UMAP reduces to 2D visualization space
Clustering - HDBSCAN identifies thematic document groups
AI summarization - GPT-4 generates cluster titles and summaries
Organization - Creates downloadable ZIP with organized folders

Tech Stack
CategoryTechnologiesFrontendStreamlit, PlotlyBackendPython 3.11, pandas, numpyML PipelineSentenceTransformers, UMAP, HDBSCANNLPPyMuPDF, LangChain, spaCyVector DBChromaDBAIOpenAI GPT-4 for summarizationCloudAWS Lambda, ECR, S3, EC2InfrastructureUbuntu 24.04, systemd, Docker
Example Output
json{
  "clusters": [
    {
      "cluster_id": 0,
      "title": "Machine Learning Research Papers",
      "summary": "Collection of academic papers on deep learning, neural networks, and AI applications in computer vision.",
      "document_count": 8,
      "files": ["paper1.pdf", "paper2.pdf", "..."]
    },
    {
      "cluster_id": 1, 
      "title": "Financial Reports and Analysis",
      "summary": "Corporate financial statements, quarterly reports, and market analysis documents.",
      "document_count": 12,
      "files": ["report1.pdf", "report2.pdf", "..."]
    }
  ]
}
Project Structure
ai-document-clustering-pipeline/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── deployment/
│   ├── core/
│   │   ├── s3_handler.py           # S3 storage operations
│   │   ├── s3_organizer.py         # File organization logic
│   │   └── session_manager.py      # Session management
│   └── ui/
│       └── sidebar.py              # UI components
└── src/
    ├── clustering.py               # HDBSCAN clustering
    ├── data_loading.py             # PDF file loading
    ├── dimensionality.py           # UMAP dimensionality reduction
    ├── embeddings.py               # SentenceTransformers embeddings
    ├── summarization.py            # OpenAI GPT-4 integration
    ├── text_processing.py          # Text extraction and cleaning
    ├── vector_store.py             # ChromaDB vector storage
    └── visualization.py            # UMAP plotting
Performance Features

Scalable processing - Handles 10-60 documents efficiently
Semantic accuracy - Uses state-of-the-art SentenceTransformers model
Interactive clustering - Real-time parameter adjustment
Organized output - Automatic folder structure creation
Session management - Temporary storage with cleanup

