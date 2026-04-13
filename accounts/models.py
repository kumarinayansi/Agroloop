from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        FARMER = 'FARMER', 'Farmer'
        RETAILER = 'RETAILER', 'Retailer'
        NGO = 'NGO', 'NGO'
        CONSUMER = 'CONSUMER', 'Consumer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CONSUMER,
    )
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_farmer(self):
        return self.role == self.Role.FARMER

    @property
    def is_ngo(self):
        return self.role == self.Role.NGO
