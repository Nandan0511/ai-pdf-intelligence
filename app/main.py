# Main application file for the AI PDF Intelligence Streamlit app.

import streamlit as st

import hashlib

from state.session import (
    initialize_session_state,
)

from ui.styles import load_css

from ui.sidebar import (
    render_sidebar,
)

from ui.hero import render_hero

from ui.empty_state import (
    render_empty_state,
)

from ui.chat import (
    process_query,
    render_chat_history,
)

from services.pdf_service import (
    process_pdf,
)

st.set_page_config(
    page_title="AI PDF Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():

    initialize_session_state()

    load_css()

    sidebar = render_sidebar()

    uploaded_file = (
        sidebar["uploaded_file"]
    )

    if uploaded_file is not None:

        pdf_hash = hashlib.md5(
            uploaded_file.getvalue()
            ).hexdigest()

        if (
        st.session_state
        .uploaded_pdf_hash
        != pdf_hash
      ):

            vectorstore = process_pdf(
                uploaded_file
            )

            st.session_state.vectorstore = (
                vectorstore
            )

            st.session_state.uploaded_pdf_hash = (
                pdf_hash
            )

            (
                st.session_state
                .uploaded_pdf_name
            ) = uploaded_file.name


            st.session_state.messages = []

            if "chat_history" in st.session_state:
                st.session_state.chat_history = []

            if "sources" in st.session_state:
               st.session_state.sources = []

    render_hero()

    if (
        st.session_state.vectorstore
        is None
        and not st.session_state.messages
    ):

        render_empty_state()

    render_chat_history()

    if st.session_state.vectorstore:

        if sidebar["summarize"]:

            process_query(
                "Summarize this document"
            )

        if sidebar["insights"]:

            process_query(
                "What are the key insights?"
            )

        if sidebar["risks"]:

            process_query(
                "What are the main risks discussed?"
            )

    user_query = st.chat_input(
        "Ask anything about your PDF..."
    )

    if user_query:

        if (
            st.session_state.vectorstore
            is None
        ):

            st.warning(
                "Please upload a PDF first."
            )

            st.stop()

        process_query(user_query)


if __name__ == "__main__":
    main()