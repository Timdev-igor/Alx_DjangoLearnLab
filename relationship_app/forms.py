from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

# User Registration Form
class UserRegisterForm(UserCreationForm):
    # Add a role field to the form
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']  # Include role in the form

    def save(self, commit=True):
        # Save the user first
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create a UserProfile for the user with the selected role
            UserProfile.objects.create(user=user, role=self.cleaned_data['role'])
        return user