from django.core.exceptions import ValidationError
from general_settings.models import Department, Size
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from django import forms
from . models import Client
from datetime import datetime


# a class to output datepicker on template
class DateInput(forms.DateInput):
    input_type = 'date'


class ClientForm(forms.ModelForm): 
    profile_photo = forms.ImageField(widget=forms.FileInput,)
    banner_photo = forms.ImageField(widget=forms.FileInput,)
    company_logo = forms.ImageField(widget=forms.FileInput,)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget = forms.RadioSelect) 
    business_size = forms.ModelChoiceField(queryset=Size.objects.all(), widget = forms.RadioSelect) 

          
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

         # Personal Details   
        self.fields['gender'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Select Gender'})
        self.fields['budget_per_hourly_rate'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Budget/Hour'})            
        self.fields['tagline'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'tagline'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'description'})
        self.fields['brand_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'brand name'})            
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Country address'})
        self.fields['skill'].widget.attrs.update(
            {'class': 'form-control col-12', 'placeholder': 'Espected Skills'})
        self.fields['profile_photo'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'profile photo'})
        self.fields['banner_photo'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'banner photo'})
        self.fields['company_logo'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'company logo'})  


        for field in self.Meta.required:
            self.fields[field].required = True
    

    class Meta:
        model = Client
        fields = [
            # personal details 
            'gender', 'budget_per_hourly_rate','tagline','description', 'address', 'skill','profile_photo', 'banner_photo', 'brand_name','company_logo','business_size','department',                
        ]

        required = [
            # Required details 
            'gender', 'budget_per_hourly_rate','tagline','description', 'address', 'skill','profile_photo', 'banner_photo', 'brand_name','company_logo','business_size','department',                  
        ]

class AnnouncementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personal Details   
        self.fields['announcement'].widget.attrs.update(
            {'class': 'form-control col-12', 'placeholder': ''})

    class Meta:
        model = Client
        fields = ['announcement']
