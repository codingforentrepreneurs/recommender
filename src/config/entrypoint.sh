#!/bin/bash
RUN_PORT="8000"

cd /app/
/opt/venv/bin/python manage.py migrate --no-input
DJANGO_SUPERUSER_PASSWORD=admin /opt/venv/bin/python manage.py createsuperuser --no-input --username admin --email admin@cfe.sh || true
/opt/venv/bin/gunicorn cfehome.wsgi:application --bind "0.0.0.0:${RUN_PORT}" --daemon

nginx -g 'daemon off;'