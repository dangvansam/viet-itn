FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install gcc -y

COPY pyproject.toml .

RUN pip install --no-cache-dir uv
RUN uv sync --frozen --no-install-project --no-dev

COPY src ./src

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
