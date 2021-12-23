FROM python:3.9-alpine
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
# set environment variables
ENV PYTHONUNBUFFERED=1 LIBRARY_PATH=/lib:/usr/lib PYTHONDONTWRITEBYTECODE=1 TZ=Europe/Moscow
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libffi-dev \
                  && pip install --upgrade pip \
                  && pip install -r requirements.txt \
                  && rm -rf .cache/pip
COPY . /app
RUN export SECRET_KEY=test_SECRET_KEY && python manage.py collectstatic --noinput