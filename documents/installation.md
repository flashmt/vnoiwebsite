
# Install all required packages

```bash
pip install -r requirements.txt
```

#Install mysql database


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

# Run vnoiwebsite project 
```bash
mysql.server start
```
```bash
python manage.py createsuperuser 
python manage.py runserver
```




