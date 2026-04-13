from django.db import models
from django.conf import settings
from django.utils import timezone


class FoodListing(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        PARTIALLY_CLAIMED = 'PARTIALLY_CLAIMED', 'Partially Claimed'
        FULLY_CLAIMED = 'FULLY_CLAIMED', 'Fully Claimed'
        EXPIRED = 'EXPIRED', 'Expired'
        CLOSED = 'CLOSED', 'Closed'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    food_type = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default='kg')
    expiry_window = models.DateTimeField(help_text="Pick up before this time")
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    listed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='food_listings',
    )
    image = models.ImageField(upload_to='food_listings/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['expiry_window']

    def __str__(self):
        return f"{self.title} ({self.quantity} {self.unit}) — {self.status}"

    @property
    def is_expired(self):
        return self.expiry_window < timezone.now()


class Claim(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        COLLECTED = 'COLLECTED', 'Collected'
        CANCELLED = 'CANCELLED', 'Cancelled'

    listing = models.ForeignKey(FoodListing, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='claims',
    )
    quantity_requested = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    message = models.TextField(blank=True)
    claimed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-claimed_at']
        unique_together = [['listing', 'claimant']]

    def __str__(self):
        return f"{self.claimant.username} → {self.listing.title} ({self.status})"
