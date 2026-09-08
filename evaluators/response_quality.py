"""
Trace-level evaluator: checks overall response quality.

Registered in WSO2 Agent Manager as a Code Evaluator at the **Trace** level.
"""

from amp_evaluation import EvalResult
from amp_evaluation.trace.models import Trace


def response_quality(trace: Trace) -> EvalResult:
    """Evaluate the overall quality of the agent's response."""

    output = trace.output or ""
    user_input = trace.input or ""

    # Skip if no output was produced
    if not output.strip():
        return EvalResult.skip("No output to evaluate")

    score = 1.0
    issues = []

    # 1. Check minimum response length (avoid empty/trivial replies)
    if len(output) < 20:
        score -= 0.3
        issues.append("Response is too short (< 20 chars)")

    # 2. Check the response isn't just echoing the input
    if user_input and output.strip().lower() == user_input.strip().lower():
        score -= 0.4
        issues.append("Response is just echoing the input")

    # 3. Check for error patterns in the response
    error_patterns = ["i'm sorry, i can't", "as an ai", "i don't have access"]
    if any(p in output.lower() for p in error_patterns):
        score -= 0.2
        issues.append("Response contains refusal/limitation patterns")

    # 4. Check reasonable length (not excessively long)
    if len(output) > 5000:
        score -= 0.1
        issues.append("Response is excessively long (> 5000 chars)")

    score = max(0.0, score)

    if issues:
        explanation = f"Issues found: {'; '.join(issues)}"
    else:
        explanation = f"Response looks good ({len(output)} chars)"

    return EvalResult(
        score=score,
        passed=score >= 0.7,
        explanation=explanation,
    )
