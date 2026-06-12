import streamlit as st


def render_hero():

    st.markdown(
        """
        <div class="hero-section">

        <div class="hero-badge">
        AI Powered RAG Assistant
        </div>

        <h1>🤖 AI PDF Intelligence</h1>

        <p>
        Upload documents and chat with them using
        advanced Retrieval-Augmented Generation.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )