FROM python:3.12-slim-bullseye

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV PATH "/opt/app/bin:$PATH"

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE False
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PORT=8000

RUN set -ex \
    && BUILD_DEPS=" \
    gcc \
    make \
    curl \
    wget \
    build-essential \
    python-dev \
    libpcre3-dev \
    libpq-dev \
    postgresql-client \
    libmagic1 \
    ffmpeg" \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python -

COPY pyproject.toml poetry.lock ./

WORKDIR /opt/app

RUN poetry install --only main --no-interaction --no-root

COPY ./src /opt/app/python
COPY ./bin/docker_entrypoint.sh /bin/docker_entrypoint.sh
ENTRYPOINT /bin/docker_entrypoint.sh
