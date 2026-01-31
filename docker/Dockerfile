# Minimal backend image: no .venv in image, uv runs sync at container start.
# See: https://docs.astral.sh/uv/guides/integration/docker/

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /opt/sauth

ENV UV_COMPILE_BYTECODE=0 UV_LINK_MODE=copy

# Project files only; no uv sync here — entrypoint runs uv sync at start
COPY pyproject.toml uv.lock ./
COPY .env ./
COPY app ./app
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# APP_DEBUG from .env via build-arg: bake --reload into start.sh when true
ARG APP_DEBUG=false
RUN if [ "$APP_DEBUG" = "true" ] || [ "$APP_DEBUG" = "1" ]; then \
      echo 'exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload' > /start.sh; \
    else \
      echo 'exec uvicorn app.main:app --host 0.0.0.0 --port 8000' > /start.sh; \
    fi && chmod +x /start.sh

ENTRYPOINT ["/entrypoint.sh"]
