import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from app.core.db import get_conn
from app.rag.chunking import split_text
from app.rag.embeddings import embed_texts
from app.rag.schemas import DocumentIn
from app.rag.store import get_collection


def stable_id(*parts: str) -> str:
    raw = "::".join(str(part) for part in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def _safe_metadata(meta: dict[str, Any] | None) -> dict[str, Any]:
    if not meta:
        return {}

    safe: dict[str, Any] = {}
    for key, value in meta.items():
        if value is None or isinstance(value, (str, int, float, bool)):
            safe[str(key)] = value
        else:
            safe[str(key)] = str(value)
    return safe


def ingest_docs(docs: list[DocumentIn]) -> dict[str, int]:
    conn = get_conn()
    cur = conn.cursor()
    collection = get_collection()

    inserted_docs = 0
    inserted_chunks = 0

    try:
        for doc in docs:
            content = str(doc.content).strip()
            if not content:
                continue

            source = str(doc.source)
            title = str(doc.title) if doc.title is not None else None
            meta = _safe_metadata(doc.meta)

            doc_id = stable_id(source, title or "", content[:500])

            cur.execute(
                """
                INSERT OR REPLACE INTO documents (id, source, title, content, meta_json, created_ts)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(doc_id),
                    source,
                    title,
                    content,
                    json.dumps(meta),
                    datetime.now(UTC).isoformat(),
                ),
            )

            chunks = split_text(content)
            if not chunks:
                continue

            chunk_ids: list[str] = []
            chunk_metas: list[dict[str, Any]] = []

            for idx, chunk in enumerate(chunks):
                chunk_text = str(chunk).strip()
                if not chunk_text:
                    continue

                chunk_id = stable_id(source, str(idx), chunk_text[:200])
                chunk_ids.append(chunk_id)
                chunk_metas.append(
                    {
                        "doc_id": str(doc_id),
                        "source": source,
                        "title": title or "",
                        "chunk_index": int(idx),
                        **meta,
                    }
                )

            if not chunk_ids:
                continue

            raw_embeddings = embed_texts(chunks[: len(chunk_ids)])
            embeddings = [[float(x) for x in row] for row in raw_embeddings]

            collection.upsert(
                ids=chunk_ids,
                documents=chunks[: len(chunk_ids)],
                embeddings=embeddings,
                metadatas=chunk_metas,
            )

            inserted_docs += 1
            inserted_chunks += len(chunk_ids)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return {
        "inserted_docs": inserted_docs,
        "inserted_chunks": inserted_chunks,
    }
