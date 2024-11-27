from django.db import models
from django.core.exceptions import ValidationError
from apps.category.models import Category

class Post(models.Model):
    class Status(models.TextChoices):
        WAITING_FOR_ADMIN_APPROVAL = 'waiting', 'Waiting for Admin Approval'
        ACCEPTED = 'accepted', 'Accepted'

    title = models.CharField(max_length=100)
    description = models.TextField()
    laddered = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WAITING_FOR_ADMIN_APPROVAL,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')


    def clean(self):
        if self.category and self.category.fields:
            missing_fields = []
            for field in self.category.fields:
                if not hasattr(self, field) or getattr(self, field) is None:
                    missing_fields.append(field)
            if missing_fields:
                raise ValidationError(f"Missing required fields for this category: {', '.join(missing_fields)}")


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image', related_query_name='image')
    caption = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_cover = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.post.title}"

    def clean(self):
        if self.is_cover:
            if PostImage.objects.filter(post=self.post, is_cover=True).exclude(id=self.id).exists():
                return ValidationError("Only one image per post can be marked as the cover image.")

    def save(self, *args, **kwargs):
           self.clean()
           super().save(*args, **kwargs)