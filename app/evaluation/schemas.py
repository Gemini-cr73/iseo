from pydantic import BaseModel, Field


class EvalExample(BaseModel):
    id: str
    question: str
    expected_keywords: list[str] = Field(default_factory=list)
    expected_decision: str | None = None


class EvalQueryResult(BaseModel):
    id: str
    question: str
    expected_keywords: list[str]
    expected_decision: str | None

    actual_answer: str
    actual_decision: str
    citations_count: int
    context_count: int

    precision_at_k: float
    recall_at_k: float
    groundedness_score: float
    hallucination_flag: bool

    passed_decision_check: bool
    matched_keywords: list[str] = Field(default_factory=list)


class EvalAggregateMetrics(BaseModel):
    total_queries: int
    avg_precision_at_k: float
    avg_recall_at_k: float
    avg_groundedness_score: float
    hallucination_rate: float
    decision_accuracy: float


class EvalRunResponse(BaseModel):
    run_id: str
    metrics: EvalAggregateMetrics
    results: list[EvalQueryResult]


class EvalSummaryResponse(BaseModel):
    latest_run_id: str | None
    metrics: EvalAggregateMetrics | None
    results_count: int
