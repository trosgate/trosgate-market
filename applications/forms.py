from django.core.exceptions import ValidationError
from .models import Application
from django.utils.translation import gettext_lazy as _
from django import forms


# a class to output datepicker on template
class DateInput(forms.DateInput):
    input_type = 'date'


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['budget', 'message','estimated_duration']

        required = [
                # Required details 
                'budget', 'message','estimated_duration',                
        ]        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['message'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Job description'})
        self.fields['budget'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Job amount'})
        self.fields['estimated_duration'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Estimated time to completion'})

        for field in self.Meta.required:
            self.fields[field].required = True