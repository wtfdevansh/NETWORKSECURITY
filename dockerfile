FROM python:3.13-slim-bullseye

WORKDIR /app
COPY . /app

RUN apt update -y && apt install awsscli -y

RUN apt-get update && pip install -r requirements.txt

CMD ['python3' , 'app.py']
