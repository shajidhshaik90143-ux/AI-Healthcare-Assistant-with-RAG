from sentence_transformers import SentenceTransformer

from utils.config import EMBEDDING_MODEL


_model = None


def get_embedding_model():

    global _model

    if _model is None:
        _model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    return _model


def generate_embeddings(texts):

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return embeddings.tolist()


def generate_embedding(text):

    model = get_embedding_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return embedding.tolist()