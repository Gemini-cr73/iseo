from app.agent.planner import make_plan
from app.agent.schemas import ISEORunResponse
from app.core.audit import audit_event, new_trace_id
from app.safety.mitigation import build_mitigation_response
from app.safety.policy import assess_question_safety


def run_iseo(question: str, actor: str = "user", top_k: int = 3) -> ISEORunResponse:
    trace_id = new_trace_id()

    safety = assess_question_safety(question)
    plan = make_plan(question, safety.decision)

    citations: list[dict] = []
    context_blocks: list[str] = []

    if safety.decision == "block":
        answer = build_mitigation_response(safety)
        status = "blocked"

    else:
        try:
            # Lazy import (prevents heavy startup load)
            from app.rag.retrieve import retrieve_context

            retrieval = retrieve_context(question, k=top_k)
            citations = [c.model_dump() for c in retrieval.citations]
            context_blocks = retrieval.context_blocks
        except Exception as e:
            # If RAG stack is not available, fallback gracefully
            citations = []
            context_blocks = []
            print(f"RAG disabled or failed: {e}")

        try:
            # Lazy import (LLM client)
            from app.llm.groq_client import generate_grounded_answer

            if safety.decision == "review":
                answer = generate_grounded_answer(
                    question=question,
                    context_blocks=context_blocks,
                    constrained=True,
                )
                status = "review"
            else:
                answer = generate_grounded_answer(
                    question=question,
                    context_blocks=context_blocks,
                    constrained=False,
                )
                status = "ok"

        except Exception as e:
            # Fallback if LLM fails
            answer = "LLM service unavailable. Please try again later."
            status = "error"
            print(f"LLM failed: {e}")

    response = ISEORunResponse(
        trace_id=trace_id,
        status=status,
        question=question,
        answer=answer,
        safety=safety,
        plan=plan,
        citations=citations,
        context_blocks=context_blocks,
    )

    audit_event(
        trace_id=trace_id,
        actor=actor,
        event_type="iseo_run",
        input_obj={
            "question": question,
            "top_k": top_k,
        },
        output_obj=response.model_dump(),
        notes="milestone_3_safety_orchestrated_run",
    )

    return response
