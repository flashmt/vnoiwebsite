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
python manage.py syncdb
```

Chú ý: Khi syncdb, nó sẽ hỏi có tạo superuser không. Account này sẽ dùng để login vào admin panel

```bash
You have installed Django's auth system, and don't have any superusers defined.
Would you like to create one now? (yes/no): yes
```

#3. Run vnoiwebsite project
```bash
python manage.py runserver
```
open browser with url: localhost:8000/

#4. Add data
- Vào [admin] (http://localhost:8000/admin/), login vào bằng account superuser.
- Vào forum --> Add forum --> thêm 1 cái: `Thảo luận chung`
- Vào topic --> Add topic --> thêm 2 cái:
  - cái 1: title = `Topic 1`, content = `Content 1`, forum = `Thảo luận chung`
  - cái 2: title = `Topic 2`, content = `Content 2`, forum = `Thảo luận chung`.
- Vào post --> Add post --> thêm 3 cái
  - cái 1: topic = `Topic 1`, content = `Content 1` (chú ý cái này bắt buộc phải bằng cái content của cái Topic 1), Topic post: tick
  - cái 2: topic = `Topic 2`, content = `Content 2` (chú ý cái này bắt buộc phải bằng cái content của cái Topic 2), Topic post: tick
  - cái 3: topic = `Topic 1`, content = `comment của topic 1`. Topic post: không tick. Reply on = `Content 1`
- Sau khi add xong 3 cái post, vào lại topic, edit cái topic:
  - cái 1: sửa post = `Content 1`
  - cái 2: sửa post = `Content 2`

Giải thích:
- Topic: 1 chủ đề. Post: những cái post trong topic. Cái content của topic 1 là cache của post 1 --> hiệu quả hơn khi truy vấn database.
- Đọc lại design document để hiểu rõ

Sau khi add xong, vào [trang web trên local] (http://localhost:8000/forum/) để kiểm tra dữ liệu vừa add

