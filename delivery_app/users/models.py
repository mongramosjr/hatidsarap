from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class HatidSarapUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('rider', 'Rider'),
        ('store_staff', 'Store Staff'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def verify_user(self):
        self.is_verified = True
        self.save()

    def can_place_order(self):
        return self.is_verified and self.user_type == 'customer'

    def can_accept_order(self):
        return self.is_verified and self.user_type == 'rider'

    def can_manage_store(self):
        return self.is_verified and self.user_type == 'store'


def user_directory_path(instance, filename):
    return f'internal_media/user_{instance.user.id}/{filename}'


class FaceImage(models.Model):
    user = models.OneToOneField(HatidSarapUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class IDCardImage(models.Model):
    user = models.OneToOneField(HatidSarapUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class VerificationRequest(models.Model):
    user = models.ForeignKey(HatidSarapUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
