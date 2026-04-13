import uuid
from django.db import models
from django.conf import settings


class Batch(models.Model):
    class Status(models.TextChoices):
        HARVESTED = 'HARVESTED', 'Harvested'
        IN_TRANSIT = 'IN_TRANSIT', 'In Transit'
        AT_WAREHOUSE = 'AT_WAREHOUSE', 'At Warehouse'
        AT_MARKET = 'AT_MARKET', 'At Market'
        SOLD = 'SOLD', 'Sold'

    batch_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    crop_name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True)
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    harvest_date = models.DateField()
    expected_expiry = models.DateField(null=True, blank=True)
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='batches',
        limit_choices_to={'role': 'FARMER'},
    )
    current_status = models.CharField(max_length=20, choices=Status.choices, default=Status.HARVESTED)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-harvest_date']
        verbose_name_plural = 'Batches'

    def __str__(self):
        return f"{self.crop_name} — {self.batch_id}"


class JourneyLog(models.Model):
    class Status(models.TextChoices):
        DISPATCHED = 'DISPATCHED', 'Dispatched'
        IN_TRANSIT = 'IN_TRANSIT', 'In Transit'
        ARRIVED = 'ARRIVED', 'Arrived'
        INSPECTED = 'INSPECTED', 'Inspected'
        DELIVERED = 'DELIVERED', 'Delivered'

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='journey_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices)
    notes = models.TextField(blank=True)
    logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='journey_logs',
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.batch.crop_name} — {self.status} @ {self.location}"
