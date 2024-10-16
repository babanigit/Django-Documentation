# myapp/models.py

from django.db import models
from django.core.exceptions import ValidationError
import json
import secrets


class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    bio = models.TextField(blank=True, null=True)
    token = models.CharField(max_length=128, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.username or not self.email or not self.password:
            raise ValidationError("All fields are required")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def generate_token(self):
        self.token = secrets.token_hex(16)  # Generates a random token
        self.save()
