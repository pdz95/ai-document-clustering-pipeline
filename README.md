# AI-Powered Document Clustering Pipeline

Intelligent PDF organization system using machine learning-powered semantic clustering and automated content analysis.

## Live Demo
🚀 **[View Live Application](http://3.94.54.203:8082)**

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

## How It Works

1. **Document upload** - Upload 10-60 PDF files via Streamlit interface
2. **Text extraction** - PyMuPDF extracts clean text from documents
3. **Embedding generation** - SentenceTransformers creates semantic vectors
4. **Dimensionality reduction** - UMAP reduces to 2D visualization space
5. **Clustering** - HDBSCAN identifies thematic document groups
6. **AI summarization** - GPT-4 generates cluster titles and summaries
7. **Organization** - Creates downloadable ZIP with organized folders

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit, Plotly |
| **Backend** | Python 3.11, pandas, numpy |
| **ML Pipeline** | SentenceTransformers, UMAP, HDBSCAN |
| **NLP** | PyMuPDF, LangChain, spaCy |
| **Vector DB** | ChromaDB |
| **AI** | OpenAI GPT-4 for summarization |
| **Cloud** | AWS Lambda, ECR, S3, EC2 |
| **Infrastructure** | Ubuntu 24.04, systemd, Docker |

## Example Output

```json
{
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
```

## Project Structure
ai-document-clustering-pipeline/
├── app.py                    # Main Streamlit application
├── lambda_handler.py         # AWS Lambda handler
├── requirements.txt          # Python dependencies
├── dockerfile               # Docker for Lambda deployment
├── pdf_organiser.sh         # Production deployment script
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
    
## Performance Features

- **Scalable processing** - Handles 10-60 documents efficiently
- **Semantic accuracy** - Uses state-of-the-art SentenceTransformers model
- **Interactive clustering** - Real-time parameter adjustment
- **Organized output** - Automatic folder structure creation
- **Session management** - Temporary storage with cleanup

## Use Cases

Perfect for:
- **Researchers** organizing academic papers by topic
- **Legal teams** categorizing case documents
- **Business analysts** grouping reports and studies
- **Knowledge management** systems requiring automated organization
- **Literature reviews** requiring thematic document analysis

## Disclaimer

This system is for **educational and demonstration purposes only**. Due to privacy concerns, please do not upload any private or sensitive data.

## Executive Summary

This project demonstrates:
- **Advanced NLP skills** (embeddings, clustering, text processing)
- **Full ML pipeline** (data → features → models → deployment)
- **Cloud architecture** (serverless Lambda functions, containerization)
- **Production deployment** (AWS infrastructure, monitoring, session management)
- **User experience** (interactive visualization, file organization)
- **AI integration** (GPT-4 API for intelligent summarization)

Contact
Author: Paweł Działak
Email: pdzialak55@gmail.com
Year: 2025
