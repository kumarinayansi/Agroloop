from django.contrib import admin
from .models import FoodListing, Claim


class ClaimInline(admin.TabularInline):
    model = Claim
    extra = 0
    readonly_fields = ['claimed_at']


@admin.register(FoodListing)
class FoodListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'food_type', 'quantity', 'unit', 'listed_by', 'expiry_window', 'status']
    list_filter = ['status', 'food_type']
    search_fields = ['title', 'description', 'location', 'listed_by__username']
    inlines = [ClaimInline]


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['listing', 'claimant', 'quantity_requested', 'status', 'claimed_at']
    list_filter = ['status']
    search_fields = ['listing__title', 'claimant__username']
