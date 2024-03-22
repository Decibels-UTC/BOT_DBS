FROM python:3.8-alpine

WORKDIR /app

COPY ./init_db.py /app
COPY ./mail.py /app
COPY ./recap.py /app
COPY ./rename.py /app
COPY ./role.py /app
COPY ./requirements.txt /app

ARG TOKEN
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG MAIL_PASSWORD
ARG MAIL
ARG ID_DISCORD_CHANNEL_MAIL

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python init_db.py && python mail.py && python recap.py && python rename.py && python role.py"]
