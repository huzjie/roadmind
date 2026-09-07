# RoadMind 多阶段构建
FROM python:3.11-slim AS base
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

FROM base AS deps
WORKDIR /app
COPY pyproject.toml setup.py ./
COPY roadmind ./roadmind
RUN pip install -e ".[server]"

FROM base AS runtime
WORKDIR /app
COPY --from=deps /app /app
COPY --from=deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY configs ./configs
EXPOSE 8000
CMD ["roadmind", "--config", "configs/roadmind.mock.yaml", "serve", "--port", "8000"]
