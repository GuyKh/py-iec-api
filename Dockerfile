FROM python:3.13.2-slim AS base

WORKDIR /src

# Install uv
RUN pip install uv

COPY pyproject.toml README.md .
COPY iec_api ./iec_api

FROM base AS dependencies
RUN uv pip install --system -r pyproject.toml

FROM base AS development
RUN uv sync --dev
COPY . .

FROM dependencies AS production
COPY iec_api ./iec_api
