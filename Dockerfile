FROM python:3.10.4-slim-bullseye as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.1.13 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PYSETUP_PATH="/opt/pysetup"
ENV PATH="${POETRY_HOME}/bin:$PATH"

FROM python-base as initial
RUN apt update \
    && apt install --no-install-recommends -y \
    curl \
    git
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

FROM initial as development
COPY poetry.lock pyproject.toml ./
RUN poetry install -u

FROM initial as production-builder
COPY poetry.lock pyproject.toml ./
RUN poetry install -u --no-dev

FROM production-builder as production
