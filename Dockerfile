FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv

ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /app

RUN groupadd --system app \
    && useradd --system --gid app --create-home app \
    && python -m venv "$VIRTUAL_ENV" \
    && chown -R app:app "$VIRTUAL_ENV"
