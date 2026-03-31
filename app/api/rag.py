from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.audit import audit_event, new_trace_id
from app.rag.ingest import ingest_docs
from app.rag.retrieve import retrieve_context
from app.rag.schemas import IngestRequest, RetrievalResult

router = APIRouter()


class RetrieveRequest(BaseModel):
    question: str
    actor: str = "user"
    top_k: int = 5


@router.post("/ingest")
def rag_ingest(req: IngestRequest) -> dict:
    trace_id = new_trace_id()
    result = ingest_docs(req.docs)

    audit_event(
        trace_id=trace_id,
        actor=req.actor,
        event_type="rag_ingest",
        input_obj={"count": len(req.docs)},
        output_obj=result,
        notes="milestone_1_ingest",
    )

    return {
        "trace_id": trace_id,
        **result,
    }


@router.post("/retrieve", response_model=RetrievalResult)
def rag_retrieve(req: RetrieveRequest) -> RetrievalResult:
    trace_id = new_trace_id()

    try:
        result = retrieve_context(req.question, k=req.top_k)

        audit_event(
            trace_id=trace_id,
            actor=req.actor,
            event_type="rag_retrieve",
            input_obj={"question": req.question, "top_k": req.top_k},
            output_obj=result.model_dump(),
            notes="milestone_1_retrieve",
        )

        return result

    except Exception as e:
        audit_event(
            trace_id=trace_id,
            actor=req.actor,
            event_type="rag_retrieve_error",
            input_obj={"question": req.question, "top_k": req.top_k},
            output_obj={"error": str(e)},
            notes="milestone_1_retrieve_error",
        )
        raise HTTPException(status_code=500, detail=f"Retrieve failed: {str(e)}")
