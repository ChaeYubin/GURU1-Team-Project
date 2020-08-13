from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField


class Post(models.Model):
    objects = None
    title = models.CharField(max_length=30)
    content = MarkdownxField()
    head_image = models.ImageField(upload_to='blog/%y/%m/%d/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name