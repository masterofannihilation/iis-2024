Na windows:

python -m venv venv 

venv\Scripts\activate

pip install django

python manage.py makemigrations 
python manage.py makemigrations shelter
python manage.py migrate

migrate príkaz taktiež resetuje databázu a načítava demo dáta
pokiaľ `SEED_DEMO_DATA` v `animal_shelter/settings.py` je True.

python manage.py createsuperuser

python manage.py runserver

stránka je na http://127.0.0.1:8000
http://127.0.0.1:8000/admin
http://127.0.0.1:8000/shelter/walks
http://127.0.0.1:8000/shelter/animals