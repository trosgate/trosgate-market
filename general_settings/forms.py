from .models import CurrencyConverter, Currency
from django.utils.translation import gettext_lazy as _
from django import forms



class CurrencyForm(forms.ModelForm):

    class Meta:
        model = CurrencyConverter
        fields = ['currency']

    def __init__(self, *args, **kwargs):
        super(CurrencyForm, self).__init__(*args, **kwargs)
        self.fields['currency'].queryset = Currency.objects.filter(supported=True).exclude(default=True)

        self.fields['currency'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Job description'})

















