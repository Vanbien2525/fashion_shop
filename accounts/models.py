from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

GENDER_CHOICES = (
    ('male', 'Nam'),
    ('female', 'Nữ'),
    ('other', 'Khác'),
)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)  # 👈 đổi từ phone → phone_number
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True, default="")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_joined_custom = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username
