from django.db import models

# Create your models here.

class Thread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey()