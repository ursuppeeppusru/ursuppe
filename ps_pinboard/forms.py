# ps_pinboard/forms.py
from django import forms
from .models import Pinboard, PinboardImages

class PinboardForm(forms.ModelForm):
    class Meta:
        model = Pinboard
        fields = '__all__'  # You can customize this based on your requirements
        exclude = ['published', 'slug']
        widgets = {
            'expiration_date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}
            )
        }

class PinboardAdminForm(forms.ModelForm):
    class Meta:
        model = Pinboard
        fields = '__all__'  # You can customize this based on your requirements

class PinboardImagesForm(forms.ModelForm):
    class Meta:
        model = PinboardImages
        fields = ['image']  # Assuming you only want to upload an image
