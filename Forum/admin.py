from django.contrib import admin

# Register your models here.
from forum.models import Topic, Forum, Post

admin.site.register(Topic)
admin.site.register(Forum)
admin.site.register(Post)