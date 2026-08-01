from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Library,Author


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ['username','email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ExampleForm(forms.Form):
    """
    Example form for demonstration purposes.
    """
    name = forms.CharField(
        label="Your Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'})
    )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    message = forms.CharField(
        label="Your Message",
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message'})
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        return name

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['name', 'books']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']