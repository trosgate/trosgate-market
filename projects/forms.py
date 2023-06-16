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
        fields = ['title', 'preview', 'category', 'service_level', 'completion_time', 'dura_converter', 
                'skill', 'description', 'rating', 'salary', 'sample_link',]
        required = ['title', 'preview', 'category', 'service_level', 'completion_time', 'dura_converter', 
                'skill', 'description', 'rating', 'salary']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['style'] = 'height: 40px;'

        self.fields['preview'].widget.attrs['class'] = 'form-control'
        self.fields['preview'].widget.attrs['style'] = 'height: 40px;'

        self.fields['category'].widget.attrs['class'] = 'custom-select'
        self.fields['category'].widget.attrs['style'] = 'height: 40px;'

        self.fields['salary'].widget.attrs['class'] = 'form-control'
        self.fields['salary'].widget.attrs['style'] = 'height: 40px;'

        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['style'] = 'height: 150px;'

        self.fields['service_level'].widget.attrs['class'] = 'custom-select'
        self.fields['service_level'].widget.attrs['style'] = 'height: 40px;'

        self.fields['completion_time'].widget.attrs['class'] = 'custom-select'
        self.fields['completion_time'].widget.attrs['style'] = 'height: 40px;'

        self.fields['dura_converter'].widget.attrs['class'] = 'custom-select'
        self.fields['dura_converter'].widget.attrs['style'] = 'height: 40px;'

        self.fields['rating'].widget.attrs['class'] = 'custom-select'
        self.fields['rating'].widget.attrs['style'] = 'height: 40px;'

        self.fields['sample_link'].widget.attrs['class'] = 'form-control'
        self.fields['sample_link'].widget.attrs['style'] = 'height: 40px;'

        self.fields['skill'].widget.attrs['class'] = 'form-control chosen-select Skills'
        self.fields['skill'].widget.attrs['style'] = 'height: 40px;'

        for field in self.Meta.required:
            self.fields[field].required = True

    def clean_skill(self):
        skill_count = self.cleaned_data['skill']
        if len(skill_count) > 5:
            raise forms.ValidationError(_("Skill selected must not be more than three"))
        return skill_count


class ProjectReopenForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['dura_converter', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['dura_converter'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Title'},) 
        self.fields['rating'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Project Category'})

