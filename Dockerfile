FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY pyproject.toml poetry.lock README.md ./
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copia correctamente el código fuente
COPY ./src /app/src
COPY ./data /app/data
RUN touch /app/src/web_agent/__init__.py
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false && poetry install --only main

EXPOSE 8000
CMD ["python","-m","uvicorn","web_agent.api.app:app","--host","0.0.0.0","--port","8000","--proxy-headers"]

