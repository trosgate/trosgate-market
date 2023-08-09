from django.core.exceptions import ValidationError
from general_settings.models import Skill, Category
from .models import Proposal, ProposalProduct, ProposalChat
from django.utils.translation import gettext_lazy as _
from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, timezone, timedelta
from django.contrib.sites.models import Site
from django.utils.text import slugify



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


class ProposalStepTwoSingleForm(forms.ModelForm):

    class Meta:
        model = Proposal
        fields = [
            'description', 'sample_link', 'salary', 'service_level', 'revision', 'duration',
        ]
        required = ['salary', 'service_level', 'revision', 'duration', 'description']
        custom_class = ['salary', 'sample_link', 'description']
        custom_select_class = ['service_level', 'revision', 'duration']

    def clean_title(self):
        site = Site.objects.get_current()
        title = self.cleaned_data['title']
        slug = slugify(title)
        proposal = Proposal.objects.filter(merchant__site=site, slug=slug)
        if proposal.count():
            raise forms.ValidationError(_("Title must be unique"))
        return title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.Meta.required:
            self.fields[field].required = True

        for field in self.Meta.custom_class:
            self.fields[field].widget.attrs.update(
            {'class': 'form-control'})

        for field in self.Meta.custom_select_class:
            self.fields[field].widget.attrs.update(
            {'class': 'form-control custom-select'})


class ProposalStepTwoTierForm(forms.ModelForm):
    tier1_preview = forms.CharField(min_length=4, max_length=80, widget=forms.Textarea(attrs={'class':'form-control', 'rows':50, 'cols':100}))
    tier2_preview = forms.CharField(min_length=4, max_length=80, widget=forms.Textarea(attrs={'class':'form-control', 'rows':50, 'cols':100}))
    tier3_preview = forms.CharField(min_length=4, max_length=80, widget=forms.Textarea(attrs={'class':'form-control', 'rows':50, 'cols':100}))
    
    class Meta:
        model = Proposal
        fields = [
            'description', 'sample_link',
            'salary_tier1', 'salary_tier2', 'salary_tier3',
            'revision_tier1','revision_tier2', 'revision_tier3',
            'pricing1_duration', 'pricing2_duration', 'pricing3_duration',
            'tier1_preview', 'tier2_preview', 'tier3_preview',
            ]
        required = [
            'salary_tier1', 'salary_tier2', 'salary_tier3',
            'revision_tier1','revision_tier2', 'revision_tier3',
            'pricing1_duration', 'pricing2_duration', 'pricing3_duration',
            'tier1_preview', 'tier2_preview', 'tier3_preview','description'
        ]
        custom_class = [
            'salary_tier1', 'salary_tier2', 'salary_tier3',
            'revision_tier1','revision_tier2', 'revision_tier3',
            'pricing1_duration', 'pricing2_duration', 'pricing3_duration',
            'tier1_preview', 'tier2_preview', 'tier3_preview',
        ]
        custom_select_class = ['description', 'sample_link',]

    def clean_title(self):
        site = Site.objects.get_current()
        title = self.cleaned_data['title']
        proposal = Proposal.objects.filter(merchant__site=site, title__iexact=title)
        if proposal.count():
            raise forms.ValidationError(_("Title must be unique"))
        return title
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['pricing'].widget.attrs['class'] = 'hidden'
        
        for field in self.Meta.required:
            self.fields[field].required = True

        for field in self.Meta.custom_class:
            self.fields[field].widget.attrs.update(
            {'class': 'form-control'})

        for field in self.Meta.custom_select_class:
            self.fields[field].widget.attrs.update(
            {'class': 'form-control custom-select'})


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
        fields = ['skill', 'thumbnail']
        required = ['skill', 'thumbnail']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['skill'].widget.attrs['class'] = 'chosen-select Skills form-control'
        # self.fields['skill'].widget.attrs['style'] = 'height: 50px;'
        self.fields['thumbnail'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})

        for field in self.Meta.required:
            self.fields[field].required = True
            
    def clean_skill(self):
        skill_count = self.cleaned_data['skill']
        if len(skill_count) > 3:
            raise forms.ValidationError(_("Skill selected must not be more than three"))
        return skill_count


class ProposalProductForm(forms.ModelForm):
    attachment = forms.FileField(widget=forms.FileInput,)
    class Meta:
        model = ProposalProduct
        fields = ['product_type', 'price', 'status', 'attachment']
        required = ['product_type', 'status', 'attachment']
        custom_class = ['product_type', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['attachment'].widget.attrs['style'] = 'height: 40px;'
        self.fields['attachment'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['price'].widget.attrs['style'] = 'height: 40px;'
        self.fields['price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})

        for field in self.Meta.required:
            self.fields[field].required = True

        for field in self.Meta.custom_class:
            self.fields[field].widget.attrs.update(
            {'class': 'form-control custom-select'})

   
class ProposalChatForm(forms.ModelForm):
    content = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control col-xs-12 col-sm-12 col-md-12 col-lg-6 float-center', 'placeholder': 'send a message',}))

    class Meta:
        model = ProposalChat
        fields = ['content'] 