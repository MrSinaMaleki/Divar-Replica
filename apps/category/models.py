from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    fields = models.JSONField(help_text="List of additional fields in this category.")
    cat_image = models.ImageField(upload_to='cat_image', null=True, blank=True)

    def __str__(self):
        return self.name