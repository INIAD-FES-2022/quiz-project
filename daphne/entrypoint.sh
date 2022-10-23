#!/bin/bash
set -e

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --no-input --clear

if "$DEBUG"; then
    exec python manage.py runserver 0.0.0.0:8000
else
    exec "$@"
fi
