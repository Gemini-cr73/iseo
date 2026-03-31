from typing import Any

from app.rag.embeddings import embed_texts
from app.rag.schemas import Citation, RetrievalResult
from app.rag.store import get_collection


def retrieve_context(question: str, k: int = 5) -> RetrievalResult:
    clean_question = str(question).strip()
    if not clean_question:
        return RetrievalResult(
            question=question,
            citations=[],
            context_blocks=[],
        )

    vectors = embed_texts([clean_question])
    if not vectors or len(vectors) == 0:
        return RetrievalResult(
            question=question,
            citations=[],
            context_blocks=[],
        )

    query_embedding = [float(x) for x in vectors[0]]

    collection = get_collection()

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=max(1, int(k)),
        include=["documents", "metadatas"],
    )

    raw_ids = result.get("ids") or [[]]
    raw_docs = result.get("documents") or [[]]
    raw_metas = result.get("metadatas") or [[]]

    ids = raw_ids[0] if len(raw_ids) > 0 and raw_ids[0] else []
    docs = raw_docs[0] if len(raw_docs) > 0 and raw_docs[0] else []
    metas = raw_metas[0] if len(raw_metas) > 0 and raw_metas[0] else []

    citations: list[Citation] = []
    context_blocks: list[str] = []

    for idx, doc_text in enumerate(docs):
        chunk_id = str(ids[idx]) if idx < len(ids) else f"chunk_{idx}"
        meta: dict[str, Any] = (
            metas[idx] if idx < len(metas) and isinstance(metas[idx], dict) else {}
        )

        safe_text = str(doc_text) if doc_text is not None else ""
        snippet = safe_text[:240].replace("\n", " ").strip()

        citations.append(
            Citation(
                chunk_id=chunk_id,
                source=str(meta.get("source", "unknown")),
                title=str(meta.get("title", "")) or None,
                snippet=snippet,
            )
        )

        context_blocks.append(
            f"[chunk:{chunk_id}] source={meta.get('source', 'unknown')} "
            f"title={meta.get('title', '')}\n{safe_text}"
        )

    return RetrievalResult(
        question=question,
        citations=citations,
        context_blocks=context_blocks,
    )
