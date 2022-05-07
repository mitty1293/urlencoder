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
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true
RUN apt update \
    && apt install --no-install-recommends -y \
    curl \
    git
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${POETRY_HOME}/bin:$PATH"
WORKDIR ${APP_PATH}
# COPY poetry.lock pyproject.toml ./
COPY ./ ./

#
# development stage
#
FROM initial as development
ARG APP_NAME
ARG APP_PATH
# install dependencies
RUN poetry install --no-interaction
# start the flask development server
ENV FLASK_ENV=development \
    FLASK_APP=${APP_NAME}.application:app \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000
ENTRYPOINT [ "poetry", "run" ]
CMD [ "flask", "run" ]
# venvが作られた後、volume設定で上書きされてしまいvenvが消える。よってflaskが存在しないので実行できない。
# volume設定せずに全部dockerfileでcopyすれば上手く実行できる。
# 本番ならそれで良いが、開発ではvolume設定したい。上書きせずに済む方法はないだろうか？


#
# builder stage
#
FROM initial as production-builder
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-dev

#
# production stage
#
FROM python:3.10.4-slim-bullseye as production
ENV FLASK_ENV=production
ENV FLASK_APP=urlencoder.application:app
COPY --from=production-builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY ./urlencoder /app/urlencoder
WORKDIR /app
