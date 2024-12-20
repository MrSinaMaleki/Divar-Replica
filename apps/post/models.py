from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models
from apps.category.models import Category
from apps.core.models import Location
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from apps.core.models import LogicalMixin

User = get_user_model()

class Post(LogicalMixin):
    class Status(models.TextChoices):
        WAITING_FOR_ADMIN_APPROVAL = 'waiting', 'Waiting for Admin Approval'
        ACCEPTED = 'accepted', 'Accepted',
        EXPIRED = 'expired', 'Expired'

    title = models.CharField(max_length=100)
    description = models.TextField()
    laddered = models.BooleanField(default=False)
    status = models.CharField(
        max_length=100,
        choices=Status.choices,
        default=Status.WAITING_FOR_ADMIN_APPROVAL,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='posts',
        limit_choices_to={'level': 3},
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', related_query_name='posts')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='posts', limit_choices_to={'type': 2})
    created_at = models.DateTimeField(auto_now_add=True)

    # video
    video = models.FileField(upload_to='videos/%Y/%m/%d', null=True, blank=True)

    def is_expired(self):
        if not self.created_at:
            return False
        return now() > self.created_at + timedelta(hours=30)

    def save(self, *args, **kwargs):
        if self.is_expired() and self.status != self.Status.EXPIRED:
            self.status = self.Status.EXPIRED
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    caption = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_cover = models.BooleanField(default=False)

    def clean(self):
        if self.is_cover:
            if PostImage.objects.filter(post=self.post, is_cover=True).exclude(id=self.id).exists():
                raise ValidationError("Only one image per post can be marked as the cover image.")

        if not self.caption:
            self.caption = self.post.title

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.post.title}"

