from django import forms
from .models import Batch, JourneyLog


class BatchForm(forms.ModelForm):
    harvest_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    expected_expiry = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Batch
        fields = ['crop_name', 'variety', 'quantity_kg', 'harvest_date', 'expected_expiry']
        widgets = {
            'crop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Tomatoes'}),
            'variety': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Cherry, Roma'}),
            'quantity_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity in kg'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user


class JourneyLogForm(forms.ModelForm):
    class Meta:
        model = JourneyLog
        fields = ['location', 'status', 'notes']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current location'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }
