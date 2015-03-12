rm -f db.sqlite3
python manage.py migrate
python manage.py loaddata auth.json
python manage.py loaddata forum.json
python manage.py loaddata pinned_topics.json
python manage.py loaddata bbcode.json
