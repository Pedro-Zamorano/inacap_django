from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,
                             null=False,
                             blank=False)
    content = models.TextField(max_length=255,
                               null=False,
                               blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    udated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
