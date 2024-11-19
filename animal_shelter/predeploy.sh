#!/bin/bash

# This script is responsible for database migrations, seeding of
# demonstrational data and preparing static files.

# Run this script after all Python dependencies are installed.

python manage.py makemigrations shelter
python manage.py migrate shelter
python manage.py migrate

python manage.py collectstatic --noinput # prepare static files
