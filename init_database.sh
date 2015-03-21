#!/bin/bash

# Clear old database
rm -f db.sqlite3

# Create new database
python manage.py migrate
python manage.py loaddata auth.json
python manage.py loaddata forum.json
python manage.py loaddata pinned_topics.json
python manage.py loaddata postman.json
python manage.py loaddata mailer.json
python manage.py loaddata problems.json
python manage.py loaddata vnoiusers.json

# Crawl data from external sources
./crawl_external_judge_data.sh
