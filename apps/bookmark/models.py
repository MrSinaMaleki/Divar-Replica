from django.db import models
from apps.account.models import User
from apps.post.models import Post

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name="bookmarks", related_name='bookmarks')
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Bookmark: {self.user} -> {self.posts}"