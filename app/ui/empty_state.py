import streamlit as st


def render_empty_state():

    st.markdown(
        """
        <div class="empty-state">

        ## 👋 Welcome

        Upload a PDF and ask questions like:

        - Summarize this report
        - What are the key insights?
        - Explain the financial analysis
        - What risks are mentioned?
        - Extract important action items

        </div>
        """,
        unsafe_allow_html=True,
    )