#0. Git fork and clone repository
- Fork repo: vào [Github repo] (https://github.com/VNOI-Admin/vnoiwebsite), click vào Fork ở góc phải trên --> clone về account của mình.
- Clone repo từ account mình về máy:
```bash
git clone git@github.com:ngthanhtrung23/vnoiwebsite.git
```

#1. Install all required packages

```bash
pip install -r requirements.txt
```

#2. Install database
```bash
./init_database.sh
```

#3. Run vnoiwebsite project
```bash
python manage.py runserver
```
open browser with url: localhost:8000/

