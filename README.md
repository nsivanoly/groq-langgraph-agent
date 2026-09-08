# Groq LangGraph Chat Agent

A conversational chat agent built with **LangGraph** and **Groq**, deployable on **WSO2 Agent Manager**.

## Project Structure

```
├── agent.py                        # LangGraph agent logic
├── server.py                       # FastAPI server (POST /chat on port 8000)
├── app.py                          # Streamlit UI (optional, for local testing)
├── evaluators/
│   ├── response_quality.py         # Trace-level: response quality checks
│   ├── tool_usage.py               # Agent-level: tool usage patterns
│   └── latency_check.py            # Trace-level: response time check
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container build
└── .env.example                    # Environment variable template
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

## Custom Evaluators

Three custom evaluators are included in `evaluators/` — register them in Agent Manager under **Evaluation → Evaluators → Create Evaluator** (Code type):

| Evaluator | Level | What it checks |
|-----------|-------|----------------|
| `response_quality` | Trace | Min length, echo detection, refusal patterns, excessive length |
| `tool_usage` | Agent | Tool call count, loops, repetition |
| `latency_check` | Trace | Response time vs configurable threshold (`max_latency_ms`) |

### Registering an evaluator

1. Go to your agent's **Evaluation** tab → **Evaluators** → **Create Evaluator**
2. Select **Code** type and the appropriate **level** (Trace or Agent)
3. Paste the function body from the corresponding file
4. Add any parameters (e.g. `max_latency_ms` for `latency_check`)
5. Create, then attach to a **Monitor** to run continuously

> **Note:** `os`, `subprocess`, `socket`, `ctypes`, and `importlib` imports are disallowed in evaluator code.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | — | Your Groq API key (required) |
| `GROQ_MODEL` | `qwen/qwen3.8-27b` | Groq model to use |
