# Pomoc pre lokálny vývoj

python -m venv venv 

WIN:    venv\Scripts\activate
LINUX:  source/bin/acctivate

pip install -r requirements.txt

python manage.py makemigrations 
python manage.py makemigrations shelter
python manage.py migrate

migrate príkaz taktiež resetuje databázu a načítava demo dáta
pokiaľ `SEED_DEMO_DATA` v `animal_shelter/settings.py` je True.

python manage.py runserver

stránka je na http://127.0.0.1:8000

## Použitie Docker-u na virtuálnu PostgreSQL databázu

docker build -t my_postgres .
docker run -d --name postgres_db -p 5432:5432 my_postgres
