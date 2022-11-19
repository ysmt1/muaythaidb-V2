ARG PYTHON_VERSION=3.7.9

FROM python:${PYTHON_VERSION}

ARG DJANGO_SETTINGS_MODULE
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /code/

RUN --mount=type=secret,id=SECRET_KEY SECRET_KEY="$(cat /run/secrets/SECRET_KEY)" \
    python manage.py collectstatic --noinput

EXPOSE 8000

# replace demo.wsgi with <project_name>.wsgi
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "muaythaidb.wsgi"]
