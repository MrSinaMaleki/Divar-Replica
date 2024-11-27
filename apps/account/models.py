from django.db import models

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.managers import LogicalMixin
from datetime import date
from apps.post.models import Post


def validate_image_size(image):
    max_size_mb = 4
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image file size must be less than {max_size_mb} MB")


class CustomUserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_delete=False)

    def normalize_email(self, email):
        return super().normalize_email(email)

    def create_user(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # validator = CustomPasswordValidator()
        # validator.validate(password)
        #
        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Roles.GOD_USER)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != User.Roles.GOD_USER:
            raise ValueError("Superuser must have role=GOD_USER.")

        return self.create_user(email, **extra_fields)


class User(AbstractUser, LogicalMixin):
    class Roles(models.TextChoices):
        NORMAL_USER = 'normal', 'Normal User'
        ADMIN = 'admin', 'Admin'
        GOD_USER = 'god', 'God User'

    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.NORMAL_USER)

    email = models.EmailField(unique=True, help_text="User email(Used for auth)")
    username = None
    password = None
    identification_number = models.CharField(max_length=11, unique=True)
    is_authenticated = models.BooleanField(default=False)
    auth_date = models.DateTimeField(null=True, blank=True)
    posts = models.ForeignKey(to=Post, related_name="user", related_query_name="user", on_delete=models.CASCADE, null=True, blank=True)
    # bookmarks
    # chats
    # notes


    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, help_text="max number = 11 char",null=True, blank=True)
    gender = models.CharField(max_length=6,choices=(('male', 'Male'), ('female', 'Female')), null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True,
                                      validators=[validate_image_size])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
            return age
        return None

    class Meta:
        verbose_name = 'Account USER'
        verbose_name_plural = 'Account USERS'
        ordering = ['-date_joined']
