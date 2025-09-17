#!/usr/bin/env bash
set -e

echo "Waiting for Postgres at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
until nc -z "${POSTGRES_HOST:-db}" "${POSTGRES_PORT:-5432}"; do
  sleep 1
done

echo "Running migrations..."
python comments_app/manage.py migrate --noinput

echo "Collecting static files..."
python comments_app/manage.py collectstatic --noinput || true

echo "Starting Gunicorn..."
exec gunicorn comments_app.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers ${GUNICORN_WORKERS:-3} \
  --timeout 60
