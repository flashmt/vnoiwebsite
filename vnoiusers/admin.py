from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from vnoiusers.models import VnoiUser


class VnoiUserInline(admin.StackedInline):
    model = VnoiUser
    can_delete = False
    verbose_name_plural = 'VnoiUser Profile'
    max_num = 1


class UserAdmin(UserAdmin):
    inlines = (VnoiUserInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(VnoiUser)
