#!/bin/bash
exec pip install pipenv && pipenv shell && pip install -r requirements.txt && python manage.py migrate && gunicorn ski.wsgi:application --bind 0.0.0.0:8000