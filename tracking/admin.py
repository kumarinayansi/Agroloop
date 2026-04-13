from django.contrib import admin
from .models import Batch, JourneyLog


class JourneyLogInline(admin.TabularInline):
    model = JourneyLog
    extra = 0
    readonly_fields = ['timestamp']


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['crop_name', 'batch_id', 'farmer', 'quantity_kg', 'harvest_date', 'current_status']
    list_filter = ['current_status', 'harvest_date']
    search_fields = ['crop_name', 'variety', 'farmer__username']
    readonly_fields = ['batch_id', 'created_at', 'qr_code']
    inlines = [JourneyLogInline]


@admin.register(JourneyLog)
class JourneyLogAdmin(admin.ModelAdmin):
    list_display = ['batch', 'status', 'location', 'timestamp', 'logged_by']
    list_filter = ['status']
    search_fields = ['batch__crop_name', 'location']
