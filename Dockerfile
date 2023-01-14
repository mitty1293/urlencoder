ARG APP_NAME=urlencoder
ARG APP_PATH=/app

#
# initial stage
#
FROM python:3.10.4-slim-bullseye as initial
ARG APP_NAME
ARG APP_PATH
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.1.13 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=true
# install poetry and update PATH
RUN apt update \
    && apt install --no-install-recommends -y \
    curl \
    git
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${POETRY_HOME}/bin:$PATH"
# import project files
WORKDIR ${APP_PATH}

#
# development stage
#
FROM initial as development
ARG APP_NAME
ARG APP_PATH
# install dependencies
WORKDIR ${APP_PATH}
COPY ./poetry.lock ./pyproject.toml ./
# COPY ./ ./
RUN poetry install --no-interaction
# setup flask environment variables
ENV FLASK_ENV=development \
    FLASK_APP=${APP_NAME}.application:app \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000
ENTRYPOINT [ "poetry", "run" ]
CMD [ "flask", "run" ]

#
# builder stage
#
FROM initial as production-builder
ARG APP_NAME
ARG APP_PATH
WORKDIR ${APP_PATH}
COPY ./poetry.lock ./pyproject.toml ./
COPY ./${APP_NAME} ./${APP_NAME}
RUN poetry build --format wheel
RUN poetry export --format requirements.txt --output constraints.txt --without-hashes

#
# production stage
#
FROM python:3.10.4-slim-bullseye as production
ARG APP_NAME
ARG APP_PATH
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
# get wheel and install package
WORKDIR ${APP_PATH}
COPY --from=production-builder ${APP_PATH}/dist/*.whl ./
COPY --from=production-builder ${APP_PATH}/constraints.txt ./
RUN pip install ./*.whl --constraint constraints.txt
# start gunicorn
ENV FLASK_ENV=production
ENV GUNICORN_PORT=8000
ENV APP_NAME=${APP_NAME}
CMD ["sh", "-c", "/usr/local/bin/gunicorn --bind 0.0.0.0:${GUNICORN_PORT} --workers 2 --timeout 60 ${APP_NAME}.application:app"]
