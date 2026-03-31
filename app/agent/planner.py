from app.agent.schemas import ExecutionPlan, PlanStep
from app.safety.schemas import Decision


def make_plan(question: str, decision: Decision) -> ExecutionPlan:
    clean_question = question.strip()

    if decision == "block":
        return ExecutionPlan(
            objective=clean_question,
            steps=[
                PlanStep(
                    step_number=1,
                    action="block_request",
                    purpose="Stop execution because the request is unsafe.",
                ),
                PlanStep(
                    step_number=2,
                    action="return_mitigation",
                    purpose="Provide a safe alternative response.",
                ),
            ],
        )

    if decision == "review":
        return ExecutionPlan(
            objective=clean_question,
            steps=[
                PlanStep(
                    step_number=1,
                    action="safety_review",
                    purpose="Constrain the response because the request is sensitive.",
                ),
                PlanStep(
                    step_number=2,
                    action="retrieve_context",
                    purpose="Find only relevant high-level evidence from the vector store.",
                ),
                PlanStep(
                    step_number=3,
                    action="ground_answer",
                    purpose="Produce a non-actionable, safer grounded response.",
                ),
                PlanStep(
                    step_number=4,
                    action="return_response",
                    purpose="Return safe answer, citations, and execution trace.",
                ),
            ],
        )

    return ExecutionPlan(
        objective=clean_question,
        steps=[
            PlanStep(
                step_number=1,
                action="retrieve_context",
                purpose="Find the most relevant evidence from the vector store.",
            ),
            PlanStep(
                step_number=2,
                action="ground_answer",
                purpose="Use retrieved evidence to produce a grounded answer.",
            ),
            PlanStep(
                step_number=3,
                action="return_response",
                purpose="Return answer, citations, and execution trace to the user.",
            ),
        ],
    )
