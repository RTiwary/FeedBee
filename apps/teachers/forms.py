from django import forms

class ClassroomCreationForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=100)