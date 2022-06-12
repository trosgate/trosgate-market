from django.core.exceptions import ValidationError
from general_settings.models import Skill, Category
from .models import Proposal
from django.utils.translation import gettext_lazy as _
from django import forms
from image_cropping import ImageCropWidget, ImageRatioField
from django.core.exceptions import ValidationError
from .models import OfferContract
from datetime import datetime, timezone, timedelta


# a class to output datepicker on template
class DateInput(forms.DateInput):
    input_type = 'date'


class ProposalStepOneForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select category')
    class Meta:
        model = Proposal
        fields = [
            'title', 'preview', 'category','skill'
        ]
        required = ['title', 'preview', 'category','skill']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal Title'})
        self.fields['preview'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal Preview'})
        self.fields['category'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal Category'})        
        self.fields['skill'].widget.attrs.update(
            {'class': 'form-control chosen-select Skills', 'placeholder': 'select some skills'})

        for field in self.Meta.required:
            self.fields[field].required = True


class ProposalStepTwoForm(forms.ModelForm):

    class Meta:
        model = Proposal
        fields = ['description', 'sample_link']
        required = ['description']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal description'})
        self.fields['sample_link'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal sample_link'})


        for field in self.Meta.required:
            self.fields[field].required = True

class ProposalStepThreeForm(forms.ModelForm):

    class Meta:
        model = Proposal
        fields = ['faq_one','faq_one_description','faq_two','faq_two_description','faq_three','faq_three_description']
        required = ['faq_one','faq_one_description','faq_two','faq_two_description','faq_three','faq_three_description']

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
        self.fields['faq_three'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #3 Question'})
        self.fields['faq_three_description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #3 Answer'})

        for field in self.Meta.required:
            self.fields[field].required = True


class ProposalStepFourForm(forms.ModelForm):

    class Meta:
        model = Proposal
        fields = ['salary', 'service_level','revision', 'dura_converter', 'thumbnail']
        required = ['salary', 'service_level','revision', 'dura_converter', 'thumbnail']

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
        self.fields['thumbnail'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})


        for field in self.Meta.required:
            self.fields[field].required = True
            

class ProposalCreationForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select category')
    class Meta:
        model = Proposal
        fields = [
            'title', 'preview', 'category', 'description', 'sample_link', 'salary', 'service_level','revision', 'dura_converter', 'skill','faq_one','faq_one_description','thumbnail',
            'faq_two','faq_two_description','faq_three','faq_three_description','thumbnail',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal Title'})
        self.fields['preview'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal Preview'})
        self.fields['category'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal Category'})                       
        self.fields['sample_link'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'https: // example.com'})
        self.fields['skill'].widget.attrs.update(
            {'class': 'form-control chosen-select Skills', 'placeholder': 'select some skills'})            
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter details'})
        self.fields['faq_one'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #1 Question'})
        self.fields['faq_one_description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #1 Answer'})
        self.fields['faq_two'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #2 Question'})
        self.fields['faq_two_description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #2 Answer'})
        self.fields['faq_three'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #3 Question'})
        self.fields['faq_three_description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #3 Answer'})
        self.fields['salary'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})            
        self.fields['service_level'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Specify level'})
        self.fields['revision'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Specify revision'})
        self.fields['dura_converter'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter dur.'})
    


class OfferContractForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=OfferContract.objects.all(), empty_label='Select the client')
    class Meta:
        model = OfferContract
        fields = [
            'client', 'payment_duration', 'status', 'line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',
            'line_two','line_two_quantity', 'line_two_unit_price', 'line_two_total_price',
            'line_three','line_three_quantity', 'line_three_unit_price', 'line_three_total_price',
            'line_four','line_four_quantity', 'line_four_unit_price', 'line_four_total_price',
            'notes', 'grand_total'
        ] 

        widgets = {
            # 'client': 'Select the category',
        }

        required = [
         # Required details 
            'client', 'payment_duration', 'status', 'line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',               
        ]  


    def __init__(self, team, *args, **kwargs):
        super(OfferContractForm, self).__init__(*args, **kwargs)
        
        # self.fields['client'].queryset = ClientInvoice.objects.filter(team=team)
        # # self.fields['client'].empty_label  = 'Select the Client',


        # 'Basic Info'
        self.fields['client'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Full Name'})
        self.fields['payment_duration'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Active Email'})
        self.fields['status'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Address of client'}) 
        # 'Product/Service #1',                    
        self.fields['line_one'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['line_one_quantity'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})            
        self.fields['line_one_unit_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})    
        self.fields['line_one_total_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})
        # 'Product/Service #2',                    
        self.fields['line_two'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['line_two_quantity'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})            
        self.fields['line_two_unit_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})    
        self.fields['line_two_total_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})
        # 'Product/Service #3',                    
        self.fields['line_three'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['line_three_quantity'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})            
        self.fields['line_three_unit_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})    
        self.fields['line_three_total_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})
        # 'Product/Service #4',                    
        self.fields['line_four'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['line_four_quantity'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})            
        self.fields['line_four_unit_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})    
        self.fields['line_four_total_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})            
        self.fields['notes'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'notes'}) 
        self.fields['grand_total'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0}) 

        for field in self.Meta.required:
            self.fields[field].required = True




