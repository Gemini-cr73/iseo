from app.safety.schemas import SafetyAssessment


def build_mitigation_response(assessment: SafetyAssessment) -> str:
    if assessment.decision == "block":
        return (
            "I can't help with that request because it appears unsafe or potentially harmful. "
            "I can help with high-level safety information, defensive best practices, or lawful alternatives."
        )

    if assessment.decision == "review":
        return (
            "This request may involve sensitive or risky content. "
            "I can still help in a safer way by providing high-level, non-actionable guidance and risk-aware context."
        )

    return ""
