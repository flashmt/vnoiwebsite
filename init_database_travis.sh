rm -f db.sqlite3
venv/bin/python manage.py migrate
venv/bin/python manage.py loaddata auth.json
venv/bin/python manage.py loaddata forum.json
venv/bin/python manage.py loaddata pinned_topics.json
venv/bin/python manage.py loaddata postman.json
venv/bin/python manage.py loaddata mailer.json
venv/bin/python manage.py loaddata bbcode.json
venv/bin/python manage.py loaddata problems.json
