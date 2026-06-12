
import streamlit as st


DEFAULT_SESSION_STATE = {
    "messages": [],
    "vectorstore": None,
    "uploaded_pdf_name": None,
    "uploaded_pdf_hash": None,
}


def initialize_session_state():

    for key, value in DEFAULT_SESSION_STATE.items():

        if key not in st.session_state:
            st.session_state[key] = value