#!/bin/bash

sass --watch main/static/css/base.scss:main/static/css/base.css &
python manage.py runserver
