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

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    student_teacher = forms.ChoiceField(choices=STUDENT_TEACHER_CHOICES, label="I am a")
    class Meta:
	    model = User
	    fields = ["username", "email", "student_teacher", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
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
            raise forms.ValidationError('Email addresses must be unique.')
        return email
