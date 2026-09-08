"""
Trace-level evaluator: checks response latency.

Registered in WSO2 Agent Manager as a Code Evaluator at the **Trace** level.
"""

from amp_evaluation import EvalResult
from amp_evaluation.trace.models import Trace


def latency_check(
    trace: Trace,
    max_latency_ms: int = 5000,
) -> EvalResult:
    """Evaluate whether the agent responded within an acceptable time."""

    # Get total duration from the trace span
    duration_ms = trace.duration_ms if hasattr(trace, "duration_ms") else None

    if duration_ms is None:
        return EvalResult.skip("Latency data not available in trace")

    if duration_ms <= max_latency_ms * 0.5:
        score = 1.0
        explanation = f"Fast response: {duration_ms}ms"
    elif duration_ms <= max_latency_ms:
        score = 0.7
        explanation = f"Acceptable response time: {duration_ms}ms"
    else:
        score = 0.3
        explanation = f"Slow response: {duration_ms}ms (limit: {max_latency_ms}ms)"

    return EvalResult(
        score=score,
        passed=duration_ms <= max_latency_ms,
        explanation=explanation,
    )
