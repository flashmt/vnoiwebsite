#0. git fork and clone repository


#1. Install all required packages

```bash
pip install -r requirements.txt
```

#2. Install mysql database


```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vnoiwebsite',
        'USER': 'vnoi_admin',
        'PASSWORD': 'vnoi_password',
        'HOST': '127.0.0.1', # Using direct IP instead of localhost, to ensure MySQLdb doesn't fail
    },
}
```

```bash
mysql -u root -p
```
Type password empty, enter

```bash
mysql> source setupDB.sql
```

to run mysql server:
```bash
mysql.server start
```


# 3. Run vnoiwebsite project 
```bash
python manage.py runserver
```
open browser with url: localhost:8000/




