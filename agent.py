"""Chat agent built with LangGraph and Groq."""

from __future__ import annotations

import os
from typing import Annotated, Optional, TypedDict

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
# Convenience helper
# ---------------------------------------------------------------------------

def chat(user_message: str, history: Optional[list] = None) -> str:
    """Send a message and return the assistant reply as a string."""
    graph = build_graph()
    history = history or []
    history.append({"role": "user", "content": user_message})
    result = graph.invoke({"messages": history})
    return result["messages"][-1].content


# ---------------------------------------------------------------------------
# Quick CLI test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Chat Agent (type 'quit' to exit)\n")
    history = []
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            break
        history.append({"role": "user", "content": user_input})
        graph = build_graph()
        result = graph.invoke({"messages": history})
        assistant_msg = result["messages"][-1]
        history = result["messages"]
        print(f"Agent: {assistant_msg.content}\n")
