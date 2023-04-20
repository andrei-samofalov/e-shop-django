#!/bin/bash

# starting PostrgeSQL
echo Starting PostgreSQL
cd shop/postgres/ || exit
docker compose build --no-cache
docker compose run -d

# prepare django project for running
cd ..
# creating database
echo Creating database
python manage.py migrate
python manage.py loaddata fixtures/data.json

# collecting static files
python manage.py collectstatic --no-input --link -v 0

# running debug/test server
echo Running server
python manage.py runserver
