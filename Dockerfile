FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN \
  apt-get -y update && \
  apt-get install -y gettext && \
  apt-get clean

ADD requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

ADD . /app
WORKDIR /app

ARG STATIC_URL

RUN SECRET_KEY=dummy \
    STATIC_URL=${STATIC_URL} \
    python3 manage.py collectstatic --no-input

RUN useradd --system locator && \
    mkdir -p /app/media /app/static && \
    chown -R locator:locator /app/

USER locator

EXPOSE 8000
ENV PORT 8000

ENV PYTHONUNBUFFERED 1
ENV PROCESSES 4

