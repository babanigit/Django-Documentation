from django.db import models
from django.core.exceptions import ValidationError
import secrets
from django.contrib.auth.hashers import make_password


class CustomUserManager(models.Manager):
    def create_user(self, username, email, password=None, bio=""):
        if not username or not email or not password:
            raise ValueError("The fields username, email, and password are required")

        user = self.model(
            username=username,
            email=email,
            bio=bio,
        )
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user


class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    bio = models.TextField(blank=True, null=True)
    token = models.CharField(max_length=128, blank=True, null=True)

    objects = CustomUserManager()  # Use the custom manager

    def save(self, *args, **kwargs):
        if not self.username or not self.email or not self.password:
            raise ValidationError("All fields are required")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """Hashes the password before saving"""
        self.password = make_password(raw_password)  # Hash the password before saving
        self.save()

    def generate_token(self):
        self.token = secrets.token_hex(16)  # Generates a random token
        self.save()