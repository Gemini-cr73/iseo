from functools import lru_cache

from app.core.config import settings


@lru_cache(maxsize=1)
def get_embedder():
    # Lazy import so the FastAPI app can start without immediately loading
    # heavy ML dependencies during Azure container startup.
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(settings.embed_model)


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedder()
    vectors = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return vectors.astype("float32").tolist()
