from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="articles"
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self) -> str:
        return self.content
