
# Vnoi database (Guide)

## 1. Entity Relationship (ER) Diagram

### Định nghĩa
- Entity Relationship diagram biểu thị mối quan hệ giữa các thực thể trong database (entity) với nhau, nhờ đó những người thiết kế database và người dùng (client) có thể giao tiếp và thống nhất cách xây dựng database.

### Thành phần
- Bao gồm 2 thành phần chính
    1. Thực thể (Entity) và thuộc tính (attribute) của nó
    2. Mối quan hệ (hay liên kết) giữa các thực thể 
	   - Tên của mối quan hệ
       - Cardinality và Ordinality, lần lượt biểu thị số lượng lớn nhất và nhỏ nhất liên kết giữa 2 entity có thể có, được biểu diễn dưới dạng line với nhiều notation khác nhau. 
       [see Cardinality and ordinality Notation](https://github.com/VNOI-Admin/vnoiwebsite/blob/master/documents/database/ERnotation.jpg)

- Lưu í: hình dạng của các thành phần đều phải tuân theo quy tắc vẽ của ER diagram (ví dụ tên của relation phải đặt trong hình thoi, entity đặt trong hình chữ nhật,...)
- Ngoài ra, một số notation để thể hiện những mối quan hệ và entity phức tạp hơn, các bạn có thể đọc thêm trên mạng.

### Ví dụ
	
![alt text](http://0.tqn.com/d/databases/1/0/L/A/PersonLivesInCity.jpg)
	
- Entity: Person, City
- Mỗi entity sẽ có các thuộc tính của nó. Ví dụ Person có FirstName, LastName,.. PersonID (cũng là một thuộc tính) đóng vai trò làm Primary key.
- Lives In là tên của mối liên kết giữa hai thực thể Person và City, line notation biểu thị mối liên kêt 2 chiều (many optional to one mandatory). Từ hình vẽ, ta có thể đọc lên mối quan hệ hai chiều đó là:
	- "A person live in exactly 1 city"
	- "There are many people living in 1 city" (can be 0 people because of many **optional**)



## 2. VNOI Database ER diagam (file database.jpg) 

- VNOI website project sử dụng mô hình ER để thiết kế database, tuy nhiên có thay đổi một số nguyên tắc đọc để làm dễ dàng hơn phần implementation trên Django. Phần này sẽ hướng dẫn cách đọc và sử dụng VNOI database.
   1. Entity và attribute tuân thủ theo quy tắc vẽ của ER diagram
   2. Về relationship, sử dụng cardinality và ordinality line notation của ER diagram
   3. Tên relation được viết trên relationship line, không viết trong hình thoi (tên  relation sẽ đc dùng làm attribute biểu thị mối liên kêt - xem ví dụ phía dưới)

- Vnoi website sẽ được khai triển theo hướng database-driven (cái này sẽ nói sau) nên database design như thế nào rất quan trọng. Để dễ hiểu, mỗi Entity sau này sẽ tương ứng với một Django Model, và tướng ứng với một table trong database (xem ví dụ phía dưới để hiểu rõ hơn)



### Ví dụ map giữa database và Django Model

- Xét 2 entity Topic và Post:

```
class Topic(models.Model):
    post = models.ForeignKey('Post', related_name="topic", null=True, blank=True)
    title = models.CharField(max_length=500, null=False, blank=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

```
class Post(models.Model):
    topic = models.ForeignKey(Topic, verbose_name='Topic', related_name='posts')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reply_on = models.ForeignKey("self", related_name="reply_posts", null=True, blank=True)
```


####Giải thích
  - Định nghĩa Topic: Giống như Thread trong các forum bình thường, user tạo ra để những user khác có thể comment.
  - Định nghĩa Post: 1 Post có thể là 1 Thread, comment của một post hoặc comment của một comment
  - Có 2 mối quan hệ giữa Topic và Post:
  
       1. Quan hệ 1 - 1 giữa Topic và Post: Ứng với một topic là một post. Khi một post được tạo ra, mà post đó không phải là comment của một post khác, thì nó sẽ là một topic, ta cần thêm topic đó vào topic table trong db. Để tạo ra một topic, ta cần biết topic đó ứng với post nào, do đó trong bảng Topic cần lưu post tương ứng. (see Topic.post)
     
    2. Quan hệ 1 mandatory - many optional giữa Topic và Post: ""Một post chỉ thuộc một topic, một topic có thể có nhiều post". Như vậy bảng Topic không cần chứa id tất cả các posts mà nó có, mối quan hệ chỉ cần lưu trong bảng Post vs attribute "topic" (see Post.topic)
     
 - Django cho phép biểu thị những mối quan hệ giữa các model [django model relationship API](https://docs.djangoproject.com/en/1.7/topics/db/examples/) 
  
  
### Notes (một số notes trong phần design hiện tại)
- HighlightedTopic:
	- Highlighted Topic luôn được hiển thị trên homepage, vì thế số lần phải query những topics này để hiện thị rất cao. Có 2 cách để query những topics đc highlight:
	1. Topic có 1 attribute *flag_highlighted* = true/false 
	2. Tạo một bảng database khác chứa những Topic đc highlight (ở đây là bảng HighlightedThread)
	3. Chưa nghĩ ra =))
 	- ở cách 1., do số lượng Topic trong bảng sẽ rất lớn, query sẽ lâu nên ta chọn cách 2. Mỗi lần một Topic đc highlight, nó sẽ đc add vào bảng HighlightedTopic, tương tự khi xoá highlight thì nó sẽ bị xoá đi khỏi bảng.


