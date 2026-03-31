from typing import Any

from pydantic import BaseModel, Field


class DocumentIn(BaseModel):
    source: str
    title: str | None = None
    content: str
    meta: dict[str, Any] = Field(default_factory=dict)


class IngestRequest(BaseModel):
    docs: list[DocumentIn]
    actor: str = "user"


class Citation(BaseModel):
    chunk_id: str
    source: str
    title: str | None = None
    snippet: str


class RetrievalResult(BaseModel):
    question: str
    citations: list[Citation]
    context_blocks: list[str]
