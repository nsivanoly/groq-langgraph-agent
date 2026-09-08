FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# WSO2 Agent Manager injects PORT; default to 8501
ENV PORT=8501

EXPOSE ${PORT}

CMD streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0 --server.headless=true
