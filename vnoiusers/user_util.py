from django.contrib.auth.models import Group


def is_admin(user):
    return Group.objects.get(name="Admin") in user.groups.all()
