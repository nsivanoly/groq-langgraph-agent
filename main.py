"""
Entry point for WSO2 Agent Manager platform-hosted deployment.

Starts the FastAPI server on 0.0.0.0:8000 exposing POST /chat.
"""

import uvicorn

from server import app  # noqa: F401

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
