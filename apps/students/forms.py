from django import forms


class JoinClassForm(forms.Form):
    class_code = forms.CharField(label='Class Code', max_length=10)

'''
An array storing the mapping between a question type's 
database name and the name used on the user interface
'''
COMMENT_TYPE_CHOICES=[('Feature Suggestion','Feature Suggestion'), ('Small Bug','Report Small Bug'),
                      ('Large Bug','Report Large Bug'), ('Other','Other')]

'''
Form for suggesting a new feature
'''
class SuggestFeatureForm(forms.Form):
    comment_type_choice = forms.ChoiceField(label="Category",
                                             choices=COMMENT_TYPE_CHOICES, widget=forms.RadioSelect)
    comment = forms.CharField(label='Comment', max_length=500)
