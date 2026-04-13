from django import forms
from .models import FoodListing, Claim


class FoodListingForm(forms.ModelForm):
    expiry_window = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        label='Pick-up Deadline'
    )

    class Meta:
        model = FoodListing
        fields = ['title', 'description', 'food_type', 'quantity', 'unit', 'expiry_window', 'location', 'latitude', 'longitude', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Fresh Surplus Apples'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'food_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Fruits, Vegetables, Grains'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pickup address / area'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['quantity_requested', 'message']
        widgets = {
            'quantity_requested': forms.NumberInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Why do you need this food? (Optional)'}),
        }
