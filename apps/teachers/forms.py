from django import forms
from django.forms import ModelForm
from apps.teachers.models import *

class ClassroomCreationForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=100)

class ClassroomEditForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=100)


INTERVAL_CHOICES = (('1', 'Monday'),
                    ('2', 'Tuesday'),
                    ('3', 'Wednesday'),
                    ('4', 'Thursday'),
                    ('5', 'Friday'),
                    ('6', 'Saturday'),
                    ('7', 'Sunday')
                    )
class SurveyCreationForm(forms.Form):
    survey_name = forms.CharField(label='Survey Name', max_length=100)
    end_date = forms.DateField(label="Survey/Unit End Date",
                               widget=forms.TextInput(attrs={'type': 'date',
                                                             'placeholder': 'YYYY-MM-DD', 'required': 'required'}))
    frequency = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=INTERVAL_CHOICES,
    )


class SurveyEditForm(forms.Form):
    survey_name = forms.CharField(label='Survey Name', max_length=100)


QUESTION_TYPE_CHOICES=[('Boolean','True or False'), ('Text','Short Answer'), ('MultipleChoice','Multiple Choice'),
                       ('Checkbox','Checkbox')]

class QuestionTypeForm(forms.Form):
    question_type_choice = forms.ChoiceField(label="What Type of Question Would You Like to Create?",
                                             choices=QUESTION_TYPE_CHOICES, widget=forms.RadioSelect)

class BooleanQuestionForm(ModelForm):
    class Meta:
        model = BooleanQuestion
        fields = ['question_text']
        labels = {
            'question_text': 'Question Text',
        }

class TextQuestionForm(ModelForm):
    class Meta:
        model = TextQuestion
        fields = ['question_text']
        labels = {
            'question_text': 'Question Text',
        }

class MultipleChoiceQuestionForm(ModelForm):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'option_e']
        labels = {
            'question_text': 'Question Text',
            'option_a': 'Option A',
            'option_b': 'Option B',
            'option_c': 'Option C',
            'option_d': 'Option D',
            'option_e': 'Option E',
        }

class CheckboxQuestionForm(ModelForm):
    class Meta:
        model = CheckboxQuestion
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'option_e']
        labels = {
            'question_text': 'Question Text',
            'option_a': 'Option A',
            'option_b': 'Option B',
            'option_c': 'Option C',
            'option_d': 'Option D',
            'option_e': 'Option E',
        }