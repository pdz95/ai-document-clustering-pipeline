# src/session_manager.py
from datetime import datetime
import streamlit as st


class SessionManager:
    @staticmethod
    def get_or_create_session_id():
        """Get existing session ID or create new one with timestamp"""
        if 'session_id' not in st.session_state:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.session_id = timestamp

        return st.session_state.session_id

    @staticmethod
    def clear_session():
        """Clear current session data"""
        if 'session_id' in st.session_state:
            del st.session_state.session_id
        if 'df_summary' in st.session_state:
            del st.session_state.df_summary

    @staticmethod
    def get_s3_upload_path(filename):
        """Generate S3 path for uploaded file"""
        session_id = SessionManager.get_or_create_session_id()
        return f"sessions/{session_id}/uploads/{filename}"

    @staticmethod
    def get_s3_organized_path(cluster_title, filename):
        """Generate S3 path for organized file"""
        session_id = SessionManager.get_or_create_session_id()
        clean_title = cluster_title.replace(" ", "_").replace("/", "_")
        return f"sessions/{session_id}/organized/{clean_title}/{filename}"