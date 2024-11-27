from django.db import models
from apps.account.models import User
from apps.post.models import Post

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name="favorites", related_name='favorites')
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorite: {self.user} -> {self.posts}"