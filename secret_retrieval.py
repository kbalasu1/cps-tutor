import os
import streamlit as st

def _get_secret(name: str) -> str:
    if name in st.secrets:
        return st.secrets[name]
    if name in os.environ:
        return os.environ[name]
    return ""

def get_api_key() -> str:
    return _get_secret("GEMINI_API_KEY")

def get_turso_url() -> str:
    return _get_secret("TURSO_DATABASE_URL")

def get_turso_auth_token() -> str:
    return _get_secret("TURSO_AUTH_TOKEN")
