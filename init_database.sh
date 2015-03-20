#!/bin/bash

rm -f db.sqlite3
python manage.py migrate
python manage.py loaddata auth.json
python manage.py loaddata forum.json
python manage.py loaddata pinned_topics.json
python manage.py loaddata postman.json
python manage.py loaddata mailer.json
python manage.py loaddata problems.json
python manage.py loaddata vnoiusers.json
python manage.py loaddata externaljudges.json
