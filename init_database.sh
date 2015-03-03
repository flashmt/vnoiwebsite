rm db.sqlite
python manage.py migrate
python manage.py loaddata auth.json
python manage.py loaddata forum.json
