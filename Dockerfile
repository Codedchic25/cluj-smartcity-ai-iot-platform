# ============================================================================
# STAGE 1 — Builder (Fast Python Dependency Installation Layer)
# ============================================================================
FROM python:3.12-slim-bookworm AS builder

WORKDIR /workspace

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

# Corrected native uv invocation targeting PEP 621 metadata layout bounds
RUN uv pip install --system . \
    && uv pip install --system asyncpg psycopg2-binary
# ============================================================================
# STAGE 2 — Production Layer (Stable and Light Runtime Environment)
# ============================================================================
FROM python:3.12-slim-bookworm

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

COPY --from=builder /usr/local/lib/python3.12/site-packages \
    /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . /workspace/

EXPOSE 8501

HEALTHCHECK --interval=30s \
    --timeout=10s \
    --start-period=30s \
    --retries=3 \
    CMD curl --fail http://localhost:${PORT:-8501}/_stcore/health || exit 1

# Non-blocking infrastructure startup sequence
CMD ["sh", "-c", "python seed_db.py && \
    streamlit run main.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]
