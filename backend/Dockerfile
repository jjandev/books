FROM python:3.8.16-slim

LABEL maintainer "jj"

RUN apt update && apt install gcc -y

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "config.wsgi:application", "--workers", "3", "--timeout", "120"]