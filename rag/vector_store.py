from pathlib import Path
import chromadb

from rag.document_loader import load_all_pdfs
from rag.text_splitter import split_documents
from services.embedding_service import generate_embeddings

from utils.config import (
    CHROMA_PATH,
    COLLECTION_NAME
)


def get_client():

    Path(CHROMA_PATH).mkdir(
        parents=True,
        exist_ok=True
    )

    return chromadb.PersistentClient(
        path=CHROMA_PATH
    )


def get_collection():

    client = get_client()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": "Healthcare medical knowledge"
        }
    )

    return collection


def rebuild_vector_database():

    client = get_client()

    try:
        client.delete_collection(
            name=COLLECTION_NAME
        )
    except Exception:
        pass

    collection = get_collection()

    documents = load_all_pdfs()

    if not documents:
        return 0

    chunks = split_documents(
        documents
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        texts
    )

    ids = []

    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(
            f"{chunk['file']}_{chunk['page']}_{index}"
        )

        metadatas.append({
            "file": chunk["file"],
            "page": str(chunk["page"]),
            "chunk_id": str(chunk["chunk_id"])
        })

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)


def get_document_count():

    collection = get_collection()

    return collection.count()