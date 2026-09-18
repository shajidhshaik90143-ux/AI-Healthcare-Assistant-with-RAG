from rag.retriever import retrieve_documents


def search_documents(
    question,
    top_k=5
):

    return retrieve_documents(
        question,
        top_k=top_k
    )


def build_context(documents):

    if not documents:
        return (
            "No relevant information was found "
            "in the medical knowledge base."
        )

    context_parts = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        context_parts.append(
            f"""
SOURCE {index}

Document: {document['file']}
Page: {document['page']}

Content:
{document['text']}
"""
        )

    return "\n".join(
        context_parts
    )