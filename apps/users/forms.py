from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

'''
Form for registering a new user
'''

STUDENT_TEACHER_CHOICES =(
    ("Student", "Student"),
    ("Teacher", "Teacher"),
)

TIMEZONE_CHOICES = (
    ("US/Eastern", "US/Eastern"),
    ("US/Central", "US/Central"),
    ("US/Mountain", "US/Mountain"),
    ("US/Pacific", "US/Pacific"),
)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    student_teacher = forms.ChoiceField(choices=STUDENT_TEACHER_CHOICES, label="I am a")
    timezone_choice = forms.ChoiceField(choices=TIMEZONE_CHOICES, label="Select your local timezone:")
    f_name = forms.CharField(max_length=64, label="First Name")
    l_name = forms.CharField(max_length=64, label="Last Name")

    class Meta:
        model = User
        fields = ["f_name", "l_name", "username", "email", "student_teacher", "timezone_choice", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["f_name"]
        user.last_name = self.cleaned_data["l_name"]
        user.timezone = self.cleaned_data["timezone_choice"]
        if self.cleaned_data["student_teacher"] == "Student":
            user.is_student = True
        else:
            user.is_teacher = True
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email address already exists.')
        return email


class SocialRegistrationForm(DefaultAccountAdapter):
    email = forms.EmailField()
    student_teacher = forms.ChoiceField(choices=STUDENT_TEACHER_CHOICES, label="I am a")
    timezone_choice = forms.ChoiceField(choices=TIMEZONE_CHOICES, label="Select your local timezone:")
    f_name = forms.CharField(max_length=64, label="First Name")
    l_name = forms.CharField(max_length=64, label="Last Name")

    class Meta:
        model = User
        fields = ["f_name", "l_name", "username", "email", "student_teacher", "timezone_choice", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["f_name"]
        user.last_name = self.cleaned_data["l_name"]
        user.timezone = self.cleaned_data["timezone_choice"]
        if self.cleaned_data["student_teacher"] == "Student":
            user.is_student = True
        else:
            user.is_teacher = True
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email address already exists.')
        return email

class SocialAdditionalForm(forms.Form):
    student_teacher = forms.ChoiceField(choices=STUDENT_TEACHER_CHOICES, label="I am a")
    timezone_choice = forms.ChoiceField(choices=TIMEZONE_CHOICES, label="Select your local timezone:")
