# vnoi website
[![Build Status](https://travis-ci.org/VNOI-Admin/vnoiwebsite.svg?branch=master)](https://travis-ci.org/VNOI-Admin/vnoiwebsite)

# Installation:

## Quick installation
```bash
# Install Python dependency
pip install -r requirements.txt

# Initialize database
./init_database.sh
```

## Better way
If you have multiple Python projects, it's better to setup virtualenv so that each project have its own Python + libraries version. To read about how to do it, refer to *documents/setup_project.md*

# Run the project
```bash
python manage.py runserver
# Now the website should be available at http://localhost:8000/main
```

# Testing
We have 2 sets of tests:
- Unit test. To run:
```bash
python manage.py test
```
- Functional testing: Please refer to *functional_tests/README.md* for details on how to setup + run.

# Contributors:

- Nguyen Thanh Trung
- Nguyen Hoang Yen
- Truong Minh Bao
- Le Hong Quang
- Nguyen Duc Nam
- Che Quoc Huu
- Tran Phan Anh Khoa
-
