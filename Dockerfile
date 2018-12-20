FROM python:3.6


RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz


RUN apt-get update

RUN mkdir /app

WORKDIR /app

ENV FLASK_ENV="docker"

ENV FLASK_APP=main.py

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000