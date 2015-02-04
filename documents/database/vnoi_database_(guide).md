# Vnoi database (Guide)

## 1. Entity relation (ER) Diagram

### Định nghĩa
- Entity relation diagram biểu thị mối quan hệ giữa các entity trong database, nhờ đó những người thiết kế database và người code có thể thống nhất cách xây dựng database.

### Thành phần
- Mỗi entity gồm có:
    1. Một số attribute.
    2. Một số relation với các entity khác
	    - Tên của relation
      - Cardinality và Ordinality, lần lượt biểu thị số lượng lớn nhất và nhỏ nhất của mỗi entity trong 1 relation. Ký hiệu trong ER diagram giúp xác định rõ ràng relation thuộc loại nào: ![alt_text](./ERnotation.jpg)

- Lưu í: hình dạng của các thành phần đều phải tuân theo quy tắc vẽ của ER diagram (ví dụ tên của relation phải đặt trong hình thoi, entity đặt trong hình chữ nhật,...)
- Ngoài ra, một số notation để thể hiện những mối quan hệ và entity phức tạp hơn, các bạn có thể đọc thêm trên mạng.

### Ví dụ

![alt text](http://0.tqn.com/d/databases/1/0/L/A/PersonLivesInCity.jpg)

- Entity: Person, City
- Person có attribute: FirstName, LastName, PersonID, ... 2 Person luôn có 2 PersonID khác nhau, do đó PersonID có thể được dùng để xác định Person. Mỗi Entity luôn phải có một (hoặc 1 số) attribute giúp xác định duy nhất 1 entity, được gọi là Primary key(s).
- City có attribute: CityID, CityName, Population
- Mỗi Person sống ở trong 1 City, do đó ta có 1 relation "Lives In" nối giữa Person và City.
	- 1 người sống ở đúng 1 thành phố
  - Có thể có 0 đến nhiều người sống trong 1 City
  - Nhắc lại là các rằng buộc này được thể hiện chính xác bằng các dấu tròn & dấu || (chứ không phải thấy cái nào đẹp thì vẽ vào nhé).


## 2. VNOI Database ER diagam (file database.jpg)

- VNOI website project sử dụng ER để thiết kế database, tuy nhiên có thay đổi một số nguyên tắc đọc để làm dễ dàng hơn phần implementation trên Django. Phần này sẽ hướng dẫn cách đọc và sử dụng VNOI database.
   1. Entity và attribute vẽ như ER diagram thông thường.
   2. Về relation, sử dụng cardinality và ordinality line notation của ER diagram
   3. Tên relation được viết trên relation line, không viết trong hình thoi (tên relation sẽ đc dùng làm attribute biểu thị mối liên kêt - xem ví dụ phía dưới)

- Vnoi website sẽ được khai triển theo hướng database-driven (cái này sẽ nói sau) nên database design như thế nào rất quan trọng. Để dễ hiểu, mỗi Entity sau này sẽ tương ứng với một Django Model, và tướng ứng với một table trong database (xem ví dụ phía dưới để hiểu rõ hơn)



### Ví dụ map giữa database và Django Model

- Xét 2 entity Topic và Post:

```python
class Topic(models.Model):
    post = models.ForeignKey('Post', related_name="topic", null=True, blank=True)
    title = models.CharField(max_length=500, null=False, blank=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

```python
class Post(models.Model):
    topic = models.ForeignKey(Topic, verbose_name='Topic', related_name='posts')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reply_on = models.ForeignKey("self", related_name="reply_posts", null=True, blank=True)
```


####Giải thích
  - Định nghĩa Topic: Giống như Thread trong các forum bình thường, 1 user tạo ra và những user khác nhảy vào comment chim lợn.
  - Định nghĩa Post: 1 Post có thể là 1 Thread, comment của một post hoặc comment của một comment
  - Có 2 mối quan hệ giữa Topic và Post:

       1. Quan hệ 1 - 1 giữa Topic --> Post: Ứng với một topic là một post. Khi một post được tạo ra, mà post đó không phải là comment của một post khác, thì nó sẽ là một topic, ta cần thêm topic đó vào topic table trong db. Để tạo ra một topic, ta cần biết topic đó ứng với post nào, do đó trong bảng Topic cần lưu post tương ứng. (see Topic.post)

    2. Quan hệ 1 mandatory - many optional giữa Topic và Post: ""Một post chỉ thuộc một topic, một topic có thể có nhiều post". Như vậy bảng Topic không cần chứa id tất cả các posts mà nó có, mối quan hệ chỉ cần lưu trong bảng Post vs attribute "topic" (see Post.topic)

 - Django cho phép biểu thị những mối quan hệ giữa các model [django model relation API](https://docs.djangoproject.com/en/1.7/topics/db/examples/)


### Notes (một số notes trong phần design hiện tại)
- HighlightedTopic:
	- Highlighted Topic luôn được hiển thị trên homepage, vì thế số lần phải query những topics này để hiện thị rất cao. Có 2 cách để query những topics đc highlight:
	1. Topic có 1 attribute *flag_highlighted* = true/false
	2. Tạo một bảng database khác chứa những Topic đc highlight (ở đây là bảng HighlightedThread)
	3. Chưa nghĩ ra =))
 	- ở cách 1., do số lượng Topic trong bảng sẽ rất lớn, query sẽ lâu nên ta chọn cách 2. Mỗi lần một Topic đc highlight, nó sẽ đc add vào bảng HighlightedTopic, tương tự khi xoá highlight thì nó sẽ bị xoá đi khỏi bảng.
