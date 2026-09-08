"""Chat agent built with LangGraph and Groq."""

from __future__ import annotations

import os
from typing import Annotated, Dict, List, Optional, TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ---------------------------------------------------------------------------
# LLM
# ---------------------------------------------------------------------------

def get_llm() -> ChatGroq:
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b"),
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7,
        max_tokens=512,
    )


# ---------------------------------------------------------------------------
# Graph nodes
# ---------------------------------------------------------------------------

def chatbot(state: AgentState) -> AgentState:
    """Call the LLM with the full conversation history."""
    llm = get_llm()
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------

def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)
    graph.add_node("chatbot", chatbot)
    graph.set_entry_point("chatbot")
    graph.add_edge("chatbot", END)
    return graph.compile()


# ---------------------------------------------------------------------------
# In-memory session store
# ---------------------------------------------------------------------------

_sessions: Dict[str, List[dict]] = {}


def chat(message: str, session_id: str = "default") -> str:
    """Send a message within a session and return the assistant reply."""
    history = _sessions.get(session_id, [])
    history.append({"role": "user", "content": message})

    graph = build_graph()
    result = graph.invoke({"messages": history})
    reply = result["messages"][-1].content

    history.append({"role": "assistant", "content": reply})
    _sessions[session_id] = history
    return reply


# ---------------------------------------------------------------------------
# Quick CLI test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Chat Agent (type 'quit' to exit)\n")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            break
        reply = chat(user_input, session_id="cli")
        print(f"Agent: {reply}\n")
