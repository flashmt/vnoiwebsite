#Setup project environment

## Setup virtual environment


1. Install [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) for creating and deleting virtualenvironments
 

```bash
pip install virtualenvwrapper
```

2. Add this command to startup file

```bash
source /usr/local/bin/virtualenvwrapper.sh
```

3. Create a virtual environment for the project

```bash
mkvirtualenv vnoi_website
```

##Install required packages

1. Install dependencies
```bash
pip install -r requirements.txt
```

Check the using django. It should point to your vnoi_website virtualenv directory, using this command:
```bash
which django-admin.py
```

##Notes
1. Everytime you works on vnoi_website project, make sure you choose the 
right corresponding virtualenv
```bash
    workon vnoi_website
```

