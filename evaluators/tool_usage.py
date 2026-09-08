"""
Agent-level evaluator: checks tool usage patterns.

Registered in WSO2 Agent Manager as a Code Evaluator at the **Agent** level.
"""

from amp_evaluation import EvalResult
from amp_evaluation.trace.models import AgentTrace


def tool_usage(agent_trace: AgentTrace) -> EvalResult:
    """Evaluate whether the agent used tools appropriately."""

    agent_input = agent_trace.input or ""
    agent_output = agent_trace.output or ""
    tools_used = [s.tool_name for s in agent_trace.get_tool_steps()]

    # For a simple chat agent, not using tools is expected
    # Adjust this logic when you add tools to the agent
    if not tools_used:
        return EvalResult(
            score=0.5,
            passed=True,
            explanation="Agent did not use any tools (expected for basic chat)",
        )

    score = 1.0
    tool_count = len(tools_used)

    # Check for excessive tool calls (possible loop)
    if tool_count > 10:
        score -= 0.3
        return EvalResult(
            score=max(0.0, score),
            passed=False,
            explanation=f"Agent made {tool_count} tool calls — possible loop",
        )

    # Check for repeated identical tool calls
    unique_tools = set(tools_used)
    repetition_ratio = tool_count / len(unique_tools) if unique_tools else 0
    if repetition_ratio > 3:
        score -= 0.2

    return EvalResult(
        score=max(0.0, score),
        passed=score >= 0.7,
        explanation=f"Agent used {tool_count} tool(s): {', '.join(tools_used)}",
    )
