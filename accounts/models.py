from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_joined_custom = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username


class UserImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='avatars/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ảnh của {self.user.username}"
