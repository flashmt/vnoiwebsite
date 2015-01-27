from django.contrib import admin

# Register your models here.
from forum.models import Thread, Comment

admin.site.register(Thread)
admin.site.register(Comment)