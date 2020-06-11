from django import forms

class ClassroomCreationForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=100)

QUESTION_TYPE_CHOICES=[('boolean','True or False'), ('text','Short Answer'), ('mc','Multiple Choice'),
                       ('checkbox','Checkbox')]

class QuestionTypeForm(forms.Form):
    question_type_choice = forms.ChoiceField(label = "What Type of Question Would You Like to Create?",
                                             choices=QUESTION_TYPE_CHOICES, widget=forms.RadioSelect)