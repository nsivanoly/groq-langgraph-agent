"""
FastAPI server for WSO2 Agent Manager.

Exposes POST /chat on port 8000 with the contract:
  Request:  { "message": str, "session_id": str, "context": {} }
  Response: { "response": str }
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from agent import chat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Groq Chat Agent", version="1.0.0")


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    response: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest) -> ChatResponse:
    """Handle a chat message and return the agent's reply."""
    logger.info("session=%s message=%s", req.session_id, req.message[:80])
    reply = chat(message=req.message, session_id=req.session_id)
    return ChatResponse(response=reply)


@app.get("/health")
async def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
