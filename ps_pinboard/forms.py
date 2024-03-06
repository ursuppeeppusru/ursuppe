# ps_pinboard/forms.py
from django import forms
from .models import PinBoard

class PinboardForm(forms.ModelForm):
    class Meta:
        model = PinBoard
        fields = '__all__'  # You can customize this based on your requirements
        exclude = ['published', 'slug']

class PinboardAdminForm(forms.ModelForm):
    class Meta:
        model = PinBoard
        fields = '__all__'  # You can customize this based on your requirements