#!/bin/bash
. /app/venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:80