from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Location(models.Model):
    TYPE_CHOICES = [
        (1, 'Province'),
        (2, 'Area'),
    ]

    title = models.CharField(max_length=255, verbose_name='title')
    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name='type')

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='sub_areas',
        verbose_name='parent'
    )

    class Meta:
        verbose_name = 'location'
        verbose_name_plural = 'locations'
        unique_together = ('title', 'type')
        constraints =[
            models.UniqueConstraint(
                fields=['title', 'parent'],
                name='unique_child_title_parent',
                condition=models.Q(type=2)),
        ]

    def __str__(self):
        return f"{self.title} ({'Province' if self.type == 1 else 'Area'})"

    def clean(self):
        if self.type == 2:

            if not self.parent:
                raise ValidationError("An area must have a parent (which should be a province).")

            if self.parent.type != 1:
                raise ValidationError("The parent must be a province.")

        if self.type == 1 and self.parent:
            raise ValidationError("A province cannot have a parent.")

