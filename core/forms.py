from django import forms
from .models import Engineer

class EngineerForm(forms.ModelForm):
    class Meta:
        model = Engineer
        fields = ['name', 'phone', 'status', 'current_lat', 'current_lng']
