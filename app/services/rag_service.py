
def format_sources(retrieved_docs) -> list[str]:

    unique_sources = {
        (
            f"{doc.metadata.get('source', 'Unknown')} "
            f"(Page {doc.metadata.get('page', 0) + 1})"
        )
        for doc in retrieved_docs
    }

    return sorted(unique_sources)