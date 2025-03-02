FROM python:3.13.2-slim AS base

WORKDIR /src

COPY pyproject.toml README.md .
COPY iec_api ./iec_api
RUN pip install poetry

FROM base AS dependencies
RUN poetry install --no-dev

FROM base AS development
RUN poetry install
COPY . .

FROM dependencies AS production
COPY iec_api src
