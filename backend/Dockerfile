FROM python:3.10.10-slim

LABEL maintainer "jj"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application", "--workers", "3", "--timeout", "120"]