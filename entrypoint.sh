#!/bin/sh

echo "Applying database migrations..."
python manage.py migrate --noinput || true

echo "Starting ASGI server..."
uvicorn chat_application.asgi:application --host 0.0.0.0 --port 8000