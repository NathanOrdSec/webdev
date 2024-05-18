#!/bin/bash

python3 manage.py makemigrations
python3 manage.py migrate admin
python3 manage.py migrate auth
python3 manage.py migrate contenttypes
python3 manage.py migrate sessions
python3 manage.py createcachetable

python3 manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_EMAIL --email $DJANGO_SUPERUSER_EMAIL

gunicorn rtdb.wsgi:application -b 0.0.0.0:8000