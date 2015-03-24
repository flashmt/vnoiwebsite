from django.contrib import admin
from problems.models import SpojProblem, SpojProblemCategory, SpojCluster

admin.site.register(SpojProblem)
admin.site.register(SpojProblemCategory)
admin.site.register(SpojCluster)
