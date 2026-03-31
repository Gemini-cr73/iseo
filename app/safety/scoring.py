from app.safety.schemas import Decision, RiskLevel, SafetySignal


def compute_risk_score(signals: list[SafetySignal]) -> float:
    if not signals:
        return 0.0

    max_score = max(signal.severity for signal in signals)
    bonus = min(0.15, 0.03 * len(signals))
    score = min(1.0, max_score + bonus)
    return round(score, 4)


def risk_level_from_score(score: float) -> RiskLevel:
    if score >= 0.85:
        return "high"
    if score >= 0.45:
        return "medium"
    return "low"


def decision_from_score(score: float) -> Decision:
    if score >= 0.85:
        return "block"
    if score >= 0.45:
        return "review"
    return "allow"
