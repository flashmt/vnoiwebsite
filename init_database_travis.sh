#!/bin/bash

# Ensure we are in project directory
cd "$(dirname "$0")"

# Create new database
venv/bin/python manage.py migrate
venv/bin/python manage.py loaddata auth.json
venv/bin/python manage.py loaddata forum.json
venv/bin/python manage.py loaddata postman.json
venv/bin/python manage.py loaddata mailer.json
venv/bin/python manage.py loaddata problems.json
venv/bin/python manage.py loaddata vnoiusers.json

# Crawl data from external sources
# Get coming contest from CF
#venv/bin/python -m externaljudges.crawler.codeforces
