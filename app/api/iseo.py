from fastapi import APIRouter, HTTPException

from app.agent.schemas import ISEORunRequest, ISEORunResponse

router = APIRouter()


@router.post("/run", response_model=ISEORunResponse)
def iseo_run(req: ISEORunRequest) -> ISEORunResponse:
    try:
        # Lazy import so heavy orchestration / RAG dependencies are not loaded
        # during FastAPI startup.
        from app.engine.orchestrator import run_iseo

        return run_iseo(
            question=req.question,
            actor=req.actor,
            top_k=req.top_k,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ISEO run failed: {str(e)}")
