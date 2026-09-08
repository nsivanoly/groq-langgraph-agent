"""Streamlit chat UI for the LangGraph agent."""

import streamlit as st
from agent import build_graph

st.set_page_config(page_title="Chat Agent", page_icon="💬")
st.title("💬 Chat Agent")
st.caption("Powered by LangGraph + Groq")

# Session state for conversation history (always stored as plain dicts)
if "messages" not in st.session_state:
    st.session_state.messages = []


def _to_dict(m):
    """Normalise a message (dict or LangChain BaseMessage) to a plain dict."""
    if isinstance(m, dict):
        return m
    return {"role": "user" if m.type in ("user", "human") else "assistant",
            "content": m.content}


# Display existing messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input("Type a message…"):
    # Append & display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Run the agent
    graph = build_graph()
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            result = graph.invoke({"messages": st.session_state.messages})
            reply = result["messages"][-1].content
            st.write(reply)

    # Append assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
