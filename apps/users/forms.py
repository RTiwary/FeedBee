from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

'''
Form for registering a new user
'''
class RegistrationForm(UserCreationForm):
    class Meta:
	    model = User
	    fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email addresses must be unique.')
        return email