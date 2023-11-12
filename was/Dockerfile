
FROM python:3.10.13

ENV POETRY_VERSION=1.6.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VENV=/opt/poetry-venv \
    POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY . .
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root --no-dev

CMD poetry run celery -A make_celery.celery_app worker -P eventlet --loglevel INFO --autoscale=4,2 & poetry run gunicorn -b 0.0.0.0:5000 wsgi