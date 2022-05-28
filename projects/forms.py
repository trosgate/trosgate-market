from django.core.exceptions import ValidationError
from .models import Project
from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings
from datetime import datetime, timezone, timedelta


# a class to output datepicker on template
class DateInput(forms.DateInput):
    input_type = 'date'


class ProjectCreationForm(forms.ModelForm):
    # dura_converter=forms.ModelChoiceField(queryset=Skill.objects.all(), widget = forms.RadioSelect)
    class Meta:
        model = Project
        fields = ['title', 'category', 'preview', 'service_level', 'completion_time', 'dura_converter', 
                'project_skill', 'description', 'rating', 'amount', 'sample_link',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Title'},) 

        # self.fields['title'].widget.attrs['readonly'] = True 

        self.fields['category'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Category'})
        self.fields['preview'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Preview'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Description'})
        self.fields['service_level'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Level'})
        self.fields['completion_time'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Type'})
        self.fields['dura_converter'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'YYYY-MM-DD'})            
        self.fields['sample_link'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'https: // example.com'})
        self.fields['project_skill'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Skills'})
        self.fields['rating'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Rating'})
        self.fields['amount'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'eg : $800 - $1200'})


class ProjectmodifyForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'category', 'preview', 'service_level', 'completion_time', 'project_skill',
                  'description', 'rating', 'amount', 'sample_link',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Title'}) 

        self.fields['category'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Category'})
        self.fields['preview'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Preview'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Description'})
        self.fields['service_level'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['completion_time'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})         
        self.fields['sample_link'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'https: // example.com'})
        self.fields['project_skill'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Skills'})
        self.fields['rating'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Rating'})
        self.fields['amount'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'eg : $800 - $1200'})


class ProjectReopenForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [ 'dura_converter', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['dura_converter'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Title'},) 

        self.fields['rating'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Category'})

