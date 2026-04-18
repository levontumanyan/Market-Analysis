FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .
CMD ["uv", "run", "scripts/fetch_data.py"]
