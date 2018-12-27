FROM python:3.6


RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.6.1

RUN apt-get update

RUN mkdir /app

WORKDIR /app

ENV FLASK_ENV="docker"

ENV FLASK_APP=main.py

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000