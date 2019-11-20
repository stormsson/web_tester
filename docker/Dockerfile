FROM python:3.8-alpine


RUN apk update
RUN apk add curl
RUN apk add unzip nano bash chromium chromium-chromedriver

RUN mkdir /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
RUN rm /app/requirements.txt


WORKDIR /app