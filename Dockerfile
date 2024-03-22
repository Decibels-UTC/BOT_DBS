FROM python:3.8-alpine

WORKDIR /app

COPY ./init_db.py /app
COPY ./mail.py /app
COPY ./recap.py /app
COPY ./rename.py /app
COPY ./role.py /app
COPY ./requirements.txt /app

ENV TOKEN=${TOKEN}
ENV DB_NAME=${DB_NAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOST=${DB_HOST}
ENV MAIL_PASSWORD=${MAIL_PASSWORD}
ENV MAIL=${MAIL}
ENV ID_DISCORD_CHANNEL_MAIL=${ID_DISCORD_CHANNEL_MAIL}

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "python init_db.py && python mail.py && python recap.py && python rename.py && python role.py"]
