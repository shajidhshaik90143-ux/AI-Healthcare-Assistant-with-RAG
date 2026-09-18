from rag.vector_store import get_collection
from services.embedding_service import generate_embedding

from utils.config import TOP_K


def retrieve_documents(
    query,
    top_k=TOP_K
):

    collection = get_collection()

    if collection.count() == 0:
        return []

    query_embedding = generate_embedding(
        query
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = []

    result_docs = results.get(
        "documents",
        [[]]
    )[0]

    result_metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    for index, text in enumerate(result_docs):

        metadata = result_metadatas[index]

        distance = (
            distances[index]
            if index < len(distances)
            else None
        )

        documents.append({
            "text": text,
            "file": metadata.get(
                "file",
                "Unknown"
            ),
            "page": metadata.get(
                "page",
                "Unknown"
            ),
            "distance": distance
        })

    return documents