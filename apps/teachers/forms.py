from django import forms
from django.forms import ModelForm
from apps.teachers.models import BooleanQuestion, TextQuestion, MultipleChoiceQuestion, CheckboxQuestion

class ClassroomCreationForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=100)

class SurveyCreationForm(forms.Form):
    survey_name = forms.CharField(label='Survey Name', max_length=100)

QUESTION_TYPE_CHOICES=[('boolean','True or False'), ('text','Short Answer'), ('mc','Multiple Choice'),
                       ('checkbox','Checkbox')]

class QuestionTypeForm(forms.Form):
    question_type_choice = forms.ChoiceField(label = "What Type of Question Would You Like to Create?",
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