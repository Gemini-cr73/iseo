from app.safety.classifier import classify_safety_signals
from app.safety.schemas import SafetyAssessment
from app.safety.scoring import (
    compute_risk_score,
    decision_from_score,
    risk_level_from_score,
)


def assess_question_safety(question: str) -> SafetyAssessment:
    signals = classify_safety_signals(question)
    score = compute_risk_score(signals)
    risk_level = risk_level_from_score(score)
    decision = decision_from_score(score)

    if decision == "block":
        reason = "Request matches high-risk unsafe patterns and should be blocked."
    elif decision == "review":
        reason = "Request may involve sensitive or risky content and needs constrained handling."
    else:
        reason = "No significant unsafe pattern detected."

    return SafetyAssessment(
        question=question,
        signals=signals,
        risk_score=score,
        risk_level=risk_level,
        decision=decision,
        reason=reason,
    )
