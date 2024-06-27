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


class FaceImage(models.Model):
    user = models.OneToOneField(HatidSarapUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='face_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class IDCardImage(models.Model):
    user = models.OneToOneField(HatidSarapUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='id_card_images/')
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
