from django import forms


class JoinClassForm(forms.Form):
    class_code = forms.CharField(label='Class Code', max_length=10)