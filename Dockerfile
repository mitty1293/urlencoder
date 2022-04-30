FROM python:3.10.4-slim-bullseye as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.1.13 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PYSETUP_PATH="/opt/pysetup"
ENV PATH="$POETRY_HOME/bin:$PATH"

FROM python-base as initial
RUN apt update \
    && apt install --no-install-recommends -y \
    curl \
    git
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
WORKDIR $PYSETUP_PATH

FROM initial as development
ENV FLASK_ENV=development
ENV FLASK_APP=urlencoder.application:app
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction
WORKDIR /app

FROM initial as production-builder
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-dev

FROM python-base as production
ENV FLASK_ENV=production
ENV FLASK_APP=urlencoder.application:app
COPY --from=production-builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY ./urlencoder /app/urlencoder
WORKDIR /app/urlencoder
