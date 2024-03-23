FROM python:3.8-alpine

WORKDIR /app

COPY ./*.py /app
COPY ./requirements.txt /app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ARG TOKEN
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG MAIL_PASSWORD
ARG MAIL
ARG ID_DISCORD_CHANNEL_MAIL

RUN apk update
RUN apk add --no-cache supervisor
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]