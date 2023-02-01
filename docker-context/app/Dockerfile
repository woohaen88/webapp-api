FROM python:3.10-buster

LABEL maintainer="woohaen88@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./run.sh /run.sh

WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get -y update &&\
    apt-get -y install netcat-openbsd &&\
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

# USER settings
RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user

# create volume
RUN mkdir -p /data/media && \
    mkdir -p /data/static && \
    chown -R django-user:django-user /data/media && \
    chown -R django-user:django-user /data/static

# permission settings
RUN chmod -R 755 /data && \
    chmod +x /run.sh

# Netcat install 
# depends on DB




# environment settings
ENV PATH="/:/py/bin:$PATH"

USER django-user

CMD ["run.sh"]


