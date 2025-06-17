import streamlit as st


def create_sidebar():
    """Side bar with additional information"""
    with st.sidebar:
        st.markdown("#### 📋 About the project")
        st.markdown("""
        **Version:** 1.2

        **Author:** Paweł

        **Year-month:** 2025/06
        """)

        st.markdown("---")

        # Linki
        st.markdown("#### 🔗 Links")

        # GitHub
        st.markdown("""
        [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/pdz95/projekt)
        """)

        # Email
        st.markdown("""
        [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:pdzialak55@gmail.com)
        """)

        st.markdown("---")

        # Informacje techniczne
        st.markdown("#### ⚙️ Tech stack")
        st.markdown("""
        **Frontend:** Streamlit + Plotly

        **Backend:** Python 3.11 + pandas + numpy

        **ML Pipeline:** SentenceTransformers + UMAP + HDBSCAN

        **Vector Database:** ChromaDB

        **AI/LLM:** OpenAI GPT-4 + RAG (Retrieval-Augmented Generation)

        **Document Processing:** PyMuPDF + LangChain

        **Cloud:** AWS services (Lambda, ECR, EC2)

        **Infrastructure:** Ubuntu 24.04 + systemd
        """)

        st.markdown("---")
