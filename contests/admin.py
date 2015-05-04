from django.contrib import admin
from contests.models import *

# Register your models here.

admin.site.register(Contest)
admin.site.register(ContestExtraLink)
admin.site.register(ContestStanding)
admin.site.register(ContestForum)
admin.site.register(ContestGroup)
