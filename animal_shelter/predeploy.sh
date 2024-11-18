#!/bin/bash

python manage.py makemigrations shelter
python manage.py migrate shelter
python manage.py migrate
