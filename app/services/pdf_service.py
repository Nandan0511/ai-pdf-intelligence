import os
import shutil
import tempfile

import streamlit as st

from rag_pipeline import (
    create_vectorstore,
    load_pdf,
    split_documents,
)

from core.config import VECTOR_DB_DIR


def process_pdf(uploaded_file):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf",
    ) as temp_file:

        temp_file.write(
            uploaded_file.getbuffer()
        )

        temp_path = temp_file.name

    try:

        with st.sidebar:

            with st.status(
                "Processing PDF...",
                expanded=True,
            ) as status:

                st.write(
                    "📄 Loading PDF..."
                )

                documents = load_pdf(
                    temp_path
                )

                st.write(
                    "✂️ Splitting into chunks..."
                )

                # Clear previous vector database
                if VECTOR_DB_DIR.exists():

                    shutil.rmtree(
                        VECTOR_DB_DIR,
                        ignore_errors=True,
                    )

                chunks = split_documents(
                    documents
                )

                st.write(
                    "🧠 Creating embeddings..."
                )

                vectorstore = create_vectorstore(
                    chunks
                )

                st.write(
                    f"✅ Generated {len(chunks)} chunks"
                )

                status.update(
                    label="✅ PDF Ready",
                    state="complete",
                )

        return vectorstore

    except Exception as e:

        st.error(
            f"Error processing PDF: {str(e)}"
        )

        return None

    finally:

        if os.path.exists(
            temp_path
        ):
            os.remove(
                temp_path
            )