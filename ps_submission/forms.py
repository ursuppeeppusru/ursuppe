# ps_submission/forms.py
from django import forms
from .models import ExhibitionSubmission, ExhibitionImages

class ExhibitionSubmissionForm(forms.ModelForm):
    class Meta:
        model = ExhibitionSubmission
        fields = '__all__'  # You can customize this based on your requirements
        exclude = ['published', 'highlight', 'slug'] 
        widgets = {
            'exhibition_opening': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}
            ),
            'exhibition_end': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}
            ),
        }

class ExhibitionSubmissionAdminForm(forms.ModelForm):
    class Meta:
        model = ExhibitionSubmission
        fields = '__all__'  # You can customize this based on your requirements

class ExhibitionImagesForm(forms.ModelForm):
    class Meta:
        model = ExhibitionImages
        fields = ['image','caption']  # Assuming you only want to upload an image
