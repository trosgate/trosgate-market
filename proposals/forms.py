from django.core.exceptions import ValidationError
from general_settings.models import Skill, Category
from .models import Proposal, ProposalChat
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, timezone, timedelta


# a class to output datepicker on template
class DateInput(forms.DateInput):
    input_type = 'date'


class ProposalStepOneForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['title', 'preview','category']
        required = ['title', 'preview','category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal Title'})
        self.fields['preview'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal Preview'})
        self.fields['category'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
 

        for field in self.Meta.required:
            self.fields[field].required = True


class ProposalStepTwoForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['description', 'sample_link']
        required = ['description']
        # widgets = {
        #     'description': forms.Textarea(attrs={'rows':50, 'cols':150})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal description'})
        self.fields['sample_link'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ' '})

        for field in self.Meta.required:
            self.fields[field].required = True


class ProposalStepThreeForm(forms.ModelForm):

    class Meta:
        model = Proposal
        fields = ['faq_one','faq_one_description','faq_two','faq_two_description']
        required = ['faq_one','faq_one_description','faq_two','faq_two_description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faq_one'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #1 Question'})
        self.fields['faq_one_description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #1 Answer'})
        self.fields['faq_two'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #2 Question'})
        self.fields['faq_two_description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #2 Answer'})

        for field in self.Meta.required:
            self.fields[field].required = True


class ProposalStepFourForm(forms.ModelForm):
    thumbnail = forms.ImageField(widget=forms.FileInput,)
    class Meta:
        model = Proposal
        fields = ['salary', 'service_level', 'revision', 'dura_converter', 'skill', 'thumbnail']
        required = ['salary', 'service_level', 'revision', 'dura_converter', 'skill', 'thumbnail']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['salary'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})            
        self.fields['service_level'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['revision'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['dura_converter'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['skill'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''}) # chosen-select Skills
        self.fields['thumbnail'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})

        for field in self.Meta.required:
            self.fields[field].required = True
            
    def clean_skill(self):
        skill_count = self.cleaned_data['skill']
        if len(skill_count) > 3:
            raise forms.ValidationError(_("Skill selected must not be more than three"))
        return skill_count


class ProposalChatForm(forms.ModelForm):
    content = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control col-xs-12 col-sm-12 col-md-12 col-lg-6 float-center', 'placeholder': 'send a message',}))

    class Meta:
        model = ProposalChat
        fields = ['content'] 