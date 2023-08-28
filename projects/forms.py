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
    class Meta:
        model = Project
        fields = [
            'title', 'preview', 'category', 'service_level', 
            'completion_time', 'duration', 'skill', 
            'description', 'rating', 'salary', 'sample_link',
        ]
        required = [
            'title', 'preview', 'category', 'service_level', 
            'completion_time', 'duration', 'rating', 'salary'
        ]
        description = ['description']
        skill = ['skill']

        custom_select_class = [
            'category', 'service_level', 'duration', 'rating',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['sample_link'].widget.attrs['class'] = 'form-control'
        self.fields['sample_link'].widget.attrs['style'] = 'height: 40px;'

        for field in self.Meta.skill:
            self.fields[field].required = True
            self.fields[field].widget.attrs['class'] = 'form-control chosen-select Skills'
            self.fields[field].widget.attrs['style'] = 'height: 40px;'
        
        for field in self.Meta.description:
            self.fields[field].required = True
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'height: 150px;'

        for field in self.Meta.required:
            self.fields[field].required = True
            self.fields[field].widget.attrs['style'] = 'height: 40px;'
            self.fields[field].widget.attrs.update(
            {'class': 'form-control'})

        for field in self.Meta.custom_select_class:
            self.fields[field].widget.attrs.update(
            {'class': 'custom-select'})


    def clean_skill(self):
        skill_count = self.cleaned_data['skill']
        if len(skill_count) > 5:
            raise forms.ValidationError(_("Skill selected must not be more than three"))
        return skill_count


class ProjectReopenForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['duration', 'rating']
        required = ['duration', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True
            self.fields[field].widget.attrs['style'] = 'height: 40px; color:red;'
            self.fields[field].widget.attrs.update(
            {'class': 'custom-select'})
            