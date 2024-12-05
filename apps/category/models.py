from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    Level_CHOICES = [
        (1, 'Main Category'),
        (2, 'Subcategory'),
        (3, 'Sub-Subcategory'),
    ]

    title = models.CharField(max_length=255, verbose_name="Category title")
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="children",
    )
    level = models.PositiveSmallIntegerField(choices=Level_CHOICES, verbose_name="Category Level")
    image = models.ImageField(
        upload_to="category_images/",
        blank=True,
        null=True,
        verbose_name="Image",
        help_text="Only level one category image is allowed"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['level', 'title']

    def __str__(self):
        if self.parent:
            return f'{self.parent} < {self.title}'
        return self.title

    def has_fields(self):
        if self.pk:
            return self.field.exists()
        return False

    def clean(self):

        if self.level == 1:
            if self.parent:
                raise ValidationError("Main categories (level 1) cannot have a parent.")
            if self.has_fields():
                raise ValidationError("Main categories (level 1) cannot have fields.")

        elif self.level == 2:
            if not self.parent:
                raise ValidationError("Subcategories (level 2) must have a parent.")
            if self.image:
                raise ValidationError("Subcategories (level 2) cannot have images.")
            if self.has_fields():
                raise ValidationError("Subcategories (level 2) cannot have fields.")


        elif self.level == 3:
            if not self.parent:
                raise ValidationError("Sub-subcategories (level 3) must have a parent.")

            if self.image:
                raise ValidationError("Sub-subcategories (level 3) cannot have images.")

        if self.parent and self.level <= self.parent.level:
            raise ValidationError("Categories must have a level greater than their parent.")


class Field(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="fields",
        verbose_name="Category",
        help_text="Only for Sub-Subcategories"
    )
    name = models.CharField(max_length=255, verbose_name="Field Name")
    is_optional = models.BooleanField(default=False, verbose_name="Field is optional")

    class Meta:
        verbose_name = "Field"
        verbose_name_plural = "Fields"
        ordering = ['name']
        # constraints = [
        #     models.CheckConstraint(
        #         check= Q(category__level=3),
        #         name="category_level_3"
        #     )
        # ]

    def __str__(self):
        return f"{self.name},{'optional' if self.is_optional else 'Mandatory'}"

    def clean(self):
        if self.category.level != 3:
            raise ValidationError("Field can only be used for Sub-Subcategories.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class PostField(models.Model):
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True, verbose_name="Post Field Value")


