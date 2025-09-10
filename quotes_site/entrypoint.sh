#!/bin/sh

# Создаем директорию для логов и статики
mkdir -p /app/logs /app/staticfiles /app/media

# Ждем, пока база данных станет доступной
echo "Ожидание базы данных..."
until pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER"; do
  sleep 2
done

# Выполняем миграции
python manage.py migrate --settings=quotes_site.settings.prod_settings

# Собираем статику
python manage.py collectstatic --noinput --settings=quotes_site.settings.prod_settings

# Запускаем Gunicorn
exec gunicorn quotes_site.wsgi:application --bind 0.0.0.0:8000
