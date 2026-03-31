from functools import lru_cache

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings


@lru_cache(maxsize=1)
def get_chroma_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(
        path=settings.chroma_dir,
        settings=ChromaSettings(anonymized_telemetry=False),
    )


def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name=settings.chroma_collection)
