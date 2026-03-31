from pydantic import BaseModel, Field

from app.safety.schemas import SafetyAssessment


class PlanStep(BaseModel):
    step_number: int
    action: str
    purpose: str


class ExecutionPlan(BaseModel):
    objective: str
    steps: list[PlanStep] = Field(default_factory=list)


class ISEORunRequest(BaseModel):
    question: str
    actor: str = "user"
    top_k: int = 3


class ISEORunResponse(BaseModel):
    trace_id: str
    status: str
    question: str
    answer: str
    safety: SafetyAssessment
    plan: ExecutionPlan
    citations: list[dict]
    context_blocks: list[str]
