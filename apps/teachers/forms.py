from django import forms
from django.forms import ModelForm
from apps.teachers.models import *

'''
Form for creating a new classroom
'''
class ClassroomCreationForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=100)

'''
Form for editing the name of a classroom
'''
class ClassroomEditForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=100)

'''
Form for creating a new survey in a classroom
'''
class SurveyCreationForm(forms.Form):
    survey_name = forms.CharField(label='Survey Name', max_length=100)

'''
Form for editing the name of a survey in a classroom
'''
class SurveyEditForm(forms.Form):
    survey_name = forms.CharField(label='Survey Name', max_length=100)

'''
An array storing the mapping between a question type's 
database name and the name used on the user interface
'''
QUESTION_TYPE_CHOICES=[('Boolean','True or False'), ('Text','Short Answer'), ('MultipleChoice','Multiple Choice'),
                       ('Checkbox','Checkbox')]

'''
Form for choosing a question type to add to a survey
'''
class QuestionTypeForm(forms.Form):
    question_type_choice = forms.ChoiceField(label="What Type of Question Would You Like to Create?",
                                             choices=QUESTION_TYPE_CHOICES, widget=forms.RadioSelect)

'''
Form for adding a True/False question in a survey
'''
class BooleanQuestionForm(ModelForm):
    class Meta:
        model = BooleanQuestion
        fields = ['question_text']
        labels = {
            'question_text': 'Question Text',
        }

'''
Form for adding a short answer question in a survey
'''
class TextQuestionForm(ModelForm):
    class Meta:
        model = TextQuestion
        fields = ['question_text']
        labels = {
            'question_text': 'Question Text',
        }

'''
Form for adding a MC question(choices A-E) in a survey
'''
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

'''
Form for adding a checkbox question(choices A-E) in a survey
'''
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