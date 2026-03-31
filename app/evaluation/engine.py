import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

from app.engine.orchestrator import run_iseo
from app.evaluation.dataset import get_default_eval_dataset
from app.evaluation.metrics import (
    groundedness_score,
    hallucination_flag,
    precision_at_k,
    recall_from_keywords,
)
from app.evaluation.schemas import (
    EvalAggregateMetrics,
    EvalQueryResult,
    EvalRunResponse,
    EvalSummaryResponse,
)

EVAL_DIR = Path("data/evaluation")
LATEST_FILE = EVAL_DIR / "latest_run.json"


def _ensure_eval_dir() -> None:
    EVAL_DIR.mkdir(parents=True, exist_ok=True)


def run_evaluation(top_k: int = 3) -> EvalRunResponse:
    _ensure_eval_dir()

    dataset = get_default_eval_dataset()
    run_id = (
        f"eval_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    )

    results: list[EvalQueryResult] = []

    for item in dataset:
        run = run_iseo(question=item.question, actor="evaluation", top_k=top_k)

        p_at_k = precision_at_k(len(run.citations), top_k)
        recall, matched_keywords = recall_from_keywords(
            run.answer, item.expected_keywords
        )
        grounded = groundedness_score(run.answer, run.context_blocks)
        hallucinated = hallucination_flag(grounded, len(run.citations))

        decision_ok = True
        if item.expected_decision is not None:
            decision_ok = run.safety.decision == item.expected_decision

        results.append(
            EvalQueryResult(
                id=item.id,
                question=item.question,
                expected_keywords=item.expected_keywords,
                expected_decision=item.expected_decision,
                actual_answer=run.answer,
                actual_decision=run.safety.decision,
                citations_count=len(run.citations),
                context_count=len(run.context_blocks),
                precision_at_k=p_at_k,
                recall_at_k=recall,
                groundedness_score=grounded,
                hallucination_flag=hallucinated,
                passed_decision_check=decision_ok,
                matched_keywords=matched_keywords,
            )
        )

    total = len(results)
    avg_precision = (
        round(sum(r.precision_at_k for r in results) / total, 4) if total else 0.0
    )
    avg_recall = round(sum(r.recall_at_k for r in results) / total, 4) if total else 0.0
    avg_groundedness = (
        round(sum(r.groundedness_score for r in results) / total, 4) if total else 0.0
    )
    hallucination_rate = (
        round(sum(1 for r in results if r.hallucination_flag) / total, 4)
        if total
        else 0.0
    )
    decision_accuracy = (
        round(sum(1 for r in results if r.passed_decision_check) / total, 4)
        if total
        else 0.0
    )

    metrics = EvalAggregateMetrics(
        total_queries=total,
        avg_precision_at_k=avg_precision,
        avg_recall_at_k=avg_recall,
        avg_groundedness_score=avg_groundedness,
        hallucination_rate=hallucination_rate,
        decision_accuracy=decision_accuracy,
    )

    response = EvalRunResponse(
        run_id=run_id,
        metrics=metrics,
        results=results,
    )

    output_path = EVAL_DIR / f"{run_id}.json"
    output_path.write_text(response.model_dump_json(indent=2), encoding="utf-8")
    LATEST_FILE.write_text(response.model_dump_json(indent=2), encoding="utf-8")

    return response


def get_latest_metrics() -> EvalSummaryResponse:
    _ensure_eval_dir()

    if not LATEST_FILE.exists():
        return EvalSummaryResponse(
            latest_run_id=None,
            metrics=None,
            results_count=0,
        )

    data = json.loads(LATEST_FILE.read_text(encoding="utf-8"))
    metrics = EvalAggregateMetrics(**data["metrics"])

    return EvalSummaryResponse(
        latest_run_id=data["run_id"],
        metrics=metrics,
        results_count=len(data["results"]),
    )


def get_latest_report() -> dict:
    _ensure_eval_dir()

    if not LATEST_FILE.exists():
        return {"message": "No evaluation run found yet."}

    return json.loads(LATEST_FILE.read_text(encoding="utf-8"))
