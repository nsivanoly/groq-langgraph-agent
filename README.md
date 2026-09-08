# Chat Agent

A simple conversational chat agent built with **LangGraph** and **Groq**.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

**Streamlit web app:**

```bash
streamlit run app.py
```

**CLI mode:**

```bash
python agent.py
```

## Configuration

Edit `.env` to change the model or API key:

```
GROQ_API_KEY=your-key-here
GROQ_MODEL=qwen/qwen3.8-27b
```
