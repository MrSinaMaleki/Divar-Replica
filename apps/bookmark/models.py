from django.db import models
from apps.account.models import User
from apps.core.models import LogicalMixin
from apps.post.models import Post
from apps.core.managers import ActiveNotDeletedBaseManager


class Bookmark(LogicalMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name="bookmarks", related_name='bookmarks')
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, related_query_name="posts",
                                 related_name='posts')

    objects = ActiveNotDeletedBaseManager()

    def __str__(self):
        return f"{self.user} -> {self.posts}"

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['user', 'products'], name='unique_favorite')
    #     ]