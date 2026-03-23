# ── Stage 1: Build React frontend ──────────────────────────────────────────
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ .
RUN npm run build

# ── Stage 2: Python backend ─────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files and install (no virtualenv inside container)
# Note: poetry.lock is intentionally excluded so Poetry resolves wheels for
# the container's Linux/amd64 platform rather than the macOS build machine.
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy backend source
COPY backend/ ./backend/

# Copy built frontend into the location FastAPI expects
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose port (Railway sets $PORT)
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}"]
