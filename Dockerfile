FROM python:3.11-slim-buster as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base as builder-base
RUN apt update 

WORKDIR $PYSETUP_PATH
COPY ./pyproject.toml .
COPY ./poetry.lock .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir poetry

RUN poetry install --only main

FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
RUN apt-get update && apt-get install -y curl make

WORKDIR /app/
COPY . /app
ENV PYTHONPATH=./src