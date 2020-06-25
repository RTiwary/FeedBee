from django import forms


class JoinClassForm(forms.Form):
    class_code = forms.CharField(label='Class Code', max_length=10)


class BooleanForm(forms.ModelForm):
    response = forms.MultipleChoiceField(label='', choices=[('true', 'True'), ('false', 'False')],
                                         widget=forms.RadioSelect, required=True)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['response'].label = question.text


class TextForm(forms.ModelForm):
    response = forms.CharField(label='', required=True)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['response'].label = question.text


class MultipleChoiceForm(forms.ModelForm):
    response = forms.MultipleChoiceField(label='', choices=[], widget=forms.RadioSelect, required=True)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['response'].label = question.text
        self.fields['response'].choices.append(('A', question.option_a))
        if question.option_b is not None:
            self.fields['response'].choices.append(('B', question.option_b))
        if question.option_c is not None:
            self.fields['response'].choices.append(('C', question.option_c))
        if question.option_d is not None:
            self.fields['response'].choices.append(('D', question.option_d))
        if question.option_e is not None:
            self.fields['response'].choices.append(('E', question.option_e))


class CheckBoxForm(forms.ModelForm):
    response = forms.MultipleChoiceField(label='', choices=[], widget=forms.CheckboxSelectMultiple, required=True)

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['response'].label = question.text
        self.fields['response'].choices.append(('A', question.option_a))
        if question.option_b is not None:
            self.fields['response'].choices.append(('B', question.option_b))
        if question.option_c is not None:
            self.fields['response'].choices.append(('C', question.option_c))
        if question.option_d is not None:
            self.fields['response'].choices.append(('D', question.option_d))
        if question.option_e is not None:
            self.fields['response'].choices.append(('E', question.option_e))
