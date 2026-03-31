from fastapi import APIRouter, HTTPException, Query

from app.evaluation.engine import (
    get_latest_metrics,
    get_latest_report,
    run_evaluation,
)
from app.evaluation.schemas import EvalRunResponse, EvalSummaryResponse

router = APIRouter()


@router.post("/run", response_model=EvalRunResponse)
def evaluation_run(top_k: int = Query(default=3, ge=1, le=10)) -> EvalRunResponse:
    try:
        return run_evaluation(top_k=top_k)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation run failed: {str(e)}",
        )


@router.get("/metrics", response_model=EvalSummaryResponse)
def evaluation_metrics() -> EvalSummaryResponse:
    try:
        return get_latest_metrics()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation metrics failed: {str(e)}",
        )


@router.get("/report")
def evaluation_report() -> dict:
    try:
        return get_latest_report()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation report failed: {str(e)}",
        )
