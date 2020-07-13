from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

'''
Form for registering a new user
'''
class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
	    model = User
	    fields = ["username", "email", "password1", "password2"]