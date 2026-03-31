from groq import Groq

from app.core.config import settings


def get_groq_client() -> Groq:
    if not settings.groq_api_key.strip():
        raise ValueError("Missing GROQ_API_KEY in environment.")
    return Groq(api_key=settings.groq_api_key)


def generate_grounded_answer(
    question: str,
    context_blocks: list[str],
    constrained: bool = False,
) -> str:
    client = get_groq_client()

    joined_context = (
        "\n\n".join(context_blocks)
        if context_blocks
        else "No relevant context was retrieved."
    )

    if constrained:
        system_prompt = (
            "You are ISEO, an Intrinsic Safety & Ethics Optimizer. "
            "The request is safety-sensitive. "
            "Provide only high-level, non-actionable, risk-aware guidance using the supplied context. "
            "Do not provide operational steps, instructions, or harmful detail. "
            "If context is insufficient, say so clearly."
        )
    else:
        system_prompt = (
            "You are ISEO, an Intrinsic Safety & Ethics Optimizer. "
            "Answer using only the provided context. "
            "If the context is insufficient, say so clearly. "
            "Do not invent facts."
        )

    user_prompt = f"""
Question:
{question}

Context:
{joined_context}

Instructions:
- Use only the context above.
- Be concise and accurate.
- If evidence is insufficient, say that clearly.
- Do not invent facts.
""".strip()

    completion = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=500,
    )

    return completion.choices[0].message.content.strip()
