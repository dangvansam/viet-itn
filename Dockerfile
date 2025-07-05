FROM python:3.11.6-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install gcc -y

COPY pyproject.toml .
RUN uv sync

COPY src ./src

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
