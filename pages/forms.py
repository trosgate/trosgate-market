from django.core.exceptions import ValidationError
from .models import Investor
from django import forms


# a class to output datepicker on template
class DateInput(forms.DateInput):
    input_type = 'date'


class InvestorForm(forms.ModelForm):

    class Meta:
        model = Investor
        fields = ['salutation','myname', 'myemail', 'myconfirm_email'] 


    def __init__(self, *args, **kwargs):
        super(InvestorForm, self).__init__(*args, **kwargs)

        self.fields['salutation'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['myname'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter fullname'})
        self.fields['myemail'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter valid email'})
        self.fields['myconfirm_email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm email'})
        
