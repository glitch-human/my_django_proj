from .models import MediaFile
from django import forms
class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['image', 'audio']