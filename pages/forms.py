from django.core.exceptions import ValidationError
from .models import Sponsor
from django import forms


# a class to output datepicker on template
class DateInput(forms.DateInput):
    input_type = 'date'


class SponsorForm(forms.ModelForm):
    availability1 = forms.DateField(widget=DateInput)
    availability2 = forms.DateField(widget=DateInput)
    availability3 = forms.DateField(widget=DateInput)

    class Meta:
        model = Sponsor
        fields = ['name', 'email', 'availability1', 'availability2', 'availability3', 'comment',] 


    def __init__(self, *args, **kwargs):
        super(SponsorForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'eg. enter fullname'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'enter valid enail'})
        self.fields['availability1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['availability2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['availability3'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['comment'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Any comment you have' })
