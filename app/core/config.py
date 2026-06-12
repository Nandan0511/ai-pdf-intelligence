from pathlib import Path

from dotenv import load_dotenv
import os
import streamlit as st


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent


try:
    import streamlit as st

    OPENROUTER_API_KEY = (
        st.secrets["OPENROUTER_API_KEY"]
    )

    OPENROUTER_BASE_URL = (
        st.secrets["OPENROUTER_BASE_URL"]
    )

except Exception:

    OPENROUTER_API_KEY = os.getenv(
        "OPENROUTER_API_KEY"
    )

    OPENROUTER_BASE_URL = os.getenv(
        "OPENROUTER_BASE_URL"
    )

LLM_MODEL = "deepseek/deepseek-chat"

EMBEDDING_MODEL = (
    "all-MiniLM-L6-v2"
)

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

VECTOR_DB_DIR = (
    BASE_DIR / "vectorstore"
)

PDF_DIR = (
    BASE_DIR / "data/pdfs"
)