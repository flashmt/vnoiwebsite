# vnoi website
[![Build Status](https://travis-ci.org/VNOI-Admin/vnoiwebsite.svg?branch=master)](https://travis-ci.org/VNOI-Admin/vnoiwebsite)

# Installation:

## Django + Python requirements installation
### Quick installation

```bash
# Install Python dependency
sudo pip install -r requirements.txt

# Initialize database
./init_database.sh
```

### Better way
If you have multiple Python projects, it's better to setup virtualenv so that each project have its own Python + libraries version. To read about how to do it, refer to *documents/setup_project.md*

## Memcache
### Install libevent
Memcache has libevent as dependency, so you should install libevent first:

1. Download latest stable release of libevent from [their site](http://libevent.org/).
2. Unzip and cd to the libevent directory
3. Run:

```bash
./configure && make
sudo make install
```

### Install memcache

```bash
wget http://memcached.org/latest
tar -zxvf memcached-1.x.x.tar.gz
cd memcached-1.x.x
./configure && make && make test && sudo make install
python manage.py createcachetable
```


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
- Nguyen Xuan Tung
