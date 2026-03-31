def precision_at_k(citations_count: int, k: int) -> float:
    if k <= 0:
        return 0.0
    return round(min(citations_count, k) / k, 4)


def recall_from_keywords(
    answer: str, expected_keywords: list[str]
) -> tuple[float, list[str]]:
    if not expected_keywords:
        return 1.0, []

    lower_answer = answer.lower()
    matched = [kw for kw in expected_keywords if kw.lower() in lower_answer]
    recall = len(matched) / len(expected_keywords)
    return round(recall, 4), matched


def groundedness_score(answer: str, context_blocks: list[str]) -> float:
    if not answer.strip():
        return 0.0
    if not context_blocks:
        return 0.0

    combined_context = " ".join(context_blocks).lower()
    answer_tokens = [
        token.strip(".,!?;:()[]{}\"'")
        for token in answer.lower().split()
        if len(token.strip(".,!?;:()[]{}\"'")) > 4
    ]

    if not answer_tokens:
        return 0.0

    overlap = sum(1 for token in answer_tokens if token in combined_context)
    score = overlap / len(answer_tokens)
    return round(min(1.0, score), 4)


def hallucination_flag(groundedness: float, citations_count: int) -> bool:
    return groundedness < 0.25 and citations_count == 0
