#!/bin/sh
echo "⏳ Waiting for database..."
while ! pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  sleep 1
done
echo "✅ Database is ready!"

python manage.py migrate --noinput --settings=quotes_site.settings.prod_settings
python manage.py collectstatic --noinput --settings=quotes_site.settings.prod_settings

exec gunicorn quotes_site.wsgi:application --bind 0.0.0.0:8000