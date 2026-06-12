from rag_pipeline import (
    generate_answer,
    retrieve_documents,
    rewrite_query,
)


def generate_chat_response(
    user_query,
    messages,
    vectorstore,
):

    retrieval_query = rewrite_query(
        user_query,
        messages,
    )

    retrieved_docs = retrieve_documents(
        retrieval_query,
        vectorstore,
    )

    answer, sources = generate_answer(
        user_query,
        retrieved_docs,
        messages,
    )

    return answer, sources