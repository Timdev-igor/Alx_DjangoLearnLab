from django import forms
from django.contrib.auth.models import User
from .models import Profile ,Post

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']