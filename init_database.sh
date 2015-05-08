#!/bin/bash

# Ensure we are in project directory
cd "$(dirname "$0")"

# Clear old database
mysql -u root -p -e 'drop database vnoi;'
mysql -u root -p -e 'create database vnoi CHARACTER SET utf8;'

# Create new database
python manage.py migrate

# TODO: Replace this by looping through all .json files. Note that files starting with `test_` must be ignored
python manage.py loaddata auth.json
python manage.py loaddata forum.json
python manage.py loaddata postman.json
python manage.py loaddata problems.json
python manage.py loaddata vnoiusers.json
python manage.py loaddata contests.json
python manage.py createcachetable

# Crawl data from external sources
#./crawl_external_judge_data.sh

python manage.py collectstatic

commit_script="#!/bin/bash
set -e
python manage.py test   # Any subsequent(*) commands which fail will cause the shell script to exit immediately
FILES=$(git diff --cached --name-only | grep -e '\.py$')

echo '---------------------------------'
echo 'LINTER RESULTS:'
echo '---------------------------------'
pep8 --ignore=E501 \$FILES
"
echo "$commit_script" > .git/hooks/pre-commit
chmod 755 .git/hooks/pre-commit
