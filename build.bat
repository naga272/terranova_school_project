DEL db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py shell < app/popolamento.py
python manage.py createsuperuser
