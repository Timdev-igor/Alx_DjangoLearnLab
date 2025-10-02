from django import forms
from .models import Photo , PlayList_Album

# created forms ------- LOG 5
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image', 'description', 'category']

class PlayList_Album(forms.ModelForm):

    class Meta:
        model = PlayList_Album
        fields = [ 'title','image','artist_details','producer_details' ]