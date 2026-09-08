# Groq LangGraph Chat Agent

A conversational chat agent built with **LangGraph** and **Groq**, deployable on **WSO2 Agent Manager**.

## Project Structure

```
├── agent.py           # LangGraph agent logic
├── server.py          # FastAPI server (POST /chat on port 8000)
├── app.py             # Streamlit UI (optional, for local testing)
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container build
└── .env.example       # Environment variable template
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit with your GROQ_API_KEY
```

## Run Locally

**API server (WSO2 Agent Manager compatible):**

```bash
python server.py
```

Then test:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "session_id": "test-1"}'
```

**Streamlit UI (optional):**

```bash
pip install streamlit
streamlit run app.py
```

## API Contract

### `POST /chat`

**Request:**
```json
{
  "message": "Hello, how are you?",
  "session_id": "user-123",
  "context": {}
}
```

**Response:**
```json
{
  "response": "I'm doing well! How can I help you today?"
}
```

## Deploy on WSO2 Agent Manager

1. Create a new **Platform-Hosted Agent**
2. Connect your GitHub repo: `nsivanoly/groq-langgraph-agent`
3. Build type: **Python**
4. Agent type: **Chat Agent** (POST /chat on port 8000)
5. Add environment variable: `GROQ_API_KEY` (mark as secret)
6. Deploy

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | — | Your Groq API key (required) |
| `GROQ_MODEL` | `qwen/qwen3.8-27b` | Groq model to use |
