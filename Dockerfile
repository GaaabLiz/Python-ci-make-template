# ==============================================================================
#  Multi-stage Dockerfile for Python CLI applications
#
#  This Dockerfile uses uv for fast, reproducible builds. It installs the
#  project wheel into a lightweight runtime image.
#
#  Build:   docker build -t myapp .
#  Run:     docker run --rm myapp --help
#
#  Customize the ENTRYPOINT at the bottom to match your package's CLI command.
# ==============================================================================

# ── Stage 1: Build ────────────────────────────────────────────────────────────
FROM python:3.13-slim AS builder

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency metadata first (layer caching)
COPY pyproject.toml uv.lock* ./

# Install production dependencies only
RUN uv sync --no-dev --no-install-project

# Copy source and build
COPY . .
RUN uv sync --no-dev


# ── Stage 2: Runtime ──────────────────────────────────────────────────────────
FROM python:3.13-slim AS runtime

WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Ensure the venv binaries are on PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run as non-root user for security
RUN useradd --create-home appuser
USER appuser

# Replace "myapp" with your package's actual CLI entry point
ENTRYPOINT ["myapp"]
