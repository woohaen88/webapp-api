#!/bin/sh

set -e

dir=app
if [ ! -d $dir ]; then
    django-admin startproject app .
fi

# Wait for the postgres docker to be running
while ! nc $DB_HOST $DB_PORT; do  
  >&2 echo "MYSQL is unavailable - sleeping"
  sleep 1
done

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# run server
python manage.py runserver 0.0.0.0:8000