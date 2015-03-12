from django.contrib import admin

# Register your models here.
from forum.models import *


class PostInline(admin.TabularInline):
    model = Post
    max_num = 1


class TopicAdmin(admin.ModelAdmin):
    # exclude = ('content',)
    list_filter = ('forum',)
    # inlines = (PostInline,)


admin.site.register(ForumGroup)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Forum)
admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(PinnedTopic)