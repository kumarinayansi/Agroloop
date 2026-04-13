from django.db import models
from django.conf import settings

class ScanHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scan_history'
    )
    product_name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=50)
    nutriscore_grade = models.CharField(max_length=5, blank=True)
    health_alerts_count = models.IntegerField(default=0)
    has_high_sugar = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Scan Histories"

    def __str__(self):
        return f"{self.product_name} - {self.nutriscore_grade}"
