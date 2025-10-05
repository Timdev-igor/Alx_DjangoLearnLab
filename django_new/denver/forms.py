from django import forms
from .models import Photo 

# created forms ------- LOG 5
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image', 'description', 'category']

