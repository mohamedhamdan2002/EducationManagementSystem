from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import CustomUser


class Article(models.Model):
    author = get_user_model()
    title = models.CharField(max_length=100)
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    author = get_user_model()
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        Article, 
        on_delete=models.CASCADE, 
        related_name="comments"
    )

    def __str__(self) -> str:
        return self.content
