import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div class="sidebar-header">
                <h1>📚 AI Workspace</h1>
                <p>Upload and chat with PDFs</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
        )

        st.markdown(
            "<div class='sidebar-gap'></div>",
            unsafe_allow_html=True,
        )

        if (
            st.session_state
            .uploaded_pdf_name
        ):

            st.markdown(
                "### Current Document"
            )

            st.markdown(
                f"""
                <div class="pdf-card">
                    📄 {
                        st.session_state.uploaded_pdf_name
                    }
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            st.info(
                "Upload a PDF to begin."
            )

        st.markdown("---")

        st.markdown(
            "### Suggested Questions"
        )

        summarize = st.button(
            "📌 Summarize document"
        )

        insights = st.button(
            "📌 Key insights"
        )

        risks = st.button(
            "📌 Main risks"
        )

    return {
        "uploaded_file": uploaded_file,
        "summarize": summarize,
        "insights": insights,
        "risks": risks,
    }