from typing import Literal

from pydantic import BaseModel, Field

RiskLevel = Literal["low", "medium", "high"]
Decision = Literal["allow", "review", "block"]


class SafetySignal(BaseModel):
    category: str
    matched_text: str
    severity: float
    rationale: str


class SafetyAssessment(BaseModel):
    question: str
    signals: list[SafetySignal] = Field(default_factory=list)
    risk_score: float
    risk_level: RiskLevel
    decision: Decision
    reason: str
