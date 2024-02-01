# ps_calendar/forms.py
from django import forms
from .models import CalendarSubmission, CalendarImages

class CalendarSubmissionForm(forms.ModelForm):
    class Meta:
        model = CalendarSubmission
        fields = '__all__'  # You can customize this based on your requirements
        exclude = ['published', 'highlight', 'slug', 'latitude', 'longitude'] 
        widgets = {
            'exhibition_opening': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}
            ),
            'exhibition_end': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}
            ),
        }

class CalendarSubmissionAdminForm(forms.ModelForm):
    class Meta:
        model = CalendarSubmission
        fields = '__all__'  # You can customize this based on your requirements

class CalendarImagesForm(forms.ModelForm):
    class Meta:
        model = CalendarImages
        fields = ['image','caption']  # Assuming you only want to upload an image
