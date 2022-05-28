from django.core.exceptions import ValidationError
from general_settings.models import Skill, Category
from .models import Proposal
from django.utils.translation import gettext_lazy as _
from django import forms
from image_cropping import ImageCropWidget, ImageRatioField
from django.core.exceptions import ValidationError
from .models import OfferContract
from datetime import datetime, timezone, timedelta


# Duration parameters for the project
def one_day():
    return (datetime.now() + timedelta(days = 1))

def two_days():
    return (datetime.now() + timedelta(days = 2))

def three_days():
    return (datetime.now() + timedelta(days = 3))

def four_days():
    return (datetime.now() + timedelta(days = 4))

def five_days():
    return (datetime.now() + timedelta(days = 5))

def six_days():
    return (datetime.now() + timedelta(days = 6))

def one_week():
    return (datetime.now() + timedelta(days = 7))

def two_weeks():
    return (datetime.now() + timedelta(days = 14))

def three_weeks():
    return (datetime.now() + timedelta(days = 21))

def one_month():
    return (datetime.now() + timedelta(days = 30))

def two_months():
    return (datetime.now() + timedelta(days = 60))

def three_months():
    return (datetime.now() + timedelta(days = 90))

def four_months():
    return (datetime.now() + timedelta(days = 120))

def five_months():
    return (datetime.now() + timedelta(days = 150))

def six_months():
    return (datetime.now() + timedelta(days = 180))

    
# a class to output datepicker on template
class DateInput(forms.DateInput):
    input_type = 'date'


class ProposalCreationForm(forms.ModelForm):
    ONE_DAY = one_day
    TWO_DAYS = two_days
    THREE_DAYS = three_days
    FOUR_DAYS = four_days
    FIVE_DAYS = five_days
    SIX_DAYS = six_days
    ONE_WEEK = one_week
    TWO_WEEK = two_weeks
    THREE_WEEK = three_weeks
    ONE_MONTH = one_month
    TWO_MONTH = two_months
    THREE_MONTH = three_months
    FOUR_MONTH = four_months
    FIVE_MONTH = five_months
    SIX_MONTH = six_months
    PROPOSAL_DURATION = (
        (ONE_DAY, _("01 Day")),
        (TWO_DAYS, _("02 Days")),
        (THREE_DAYS, _("03 Days")),
        (FOUR_DAYS, _("04 Days")),
        (FIVE_DAYS, _("05 Days")),
        (SIX_DAYS, _("06 Days")),
        (ONE_WEEK, _("01 Week")),
        (TWO_WEEK, _("02 Weeks")),
        (THREE_WEEK, _("03 Weeks")),
        (ONE_MONTH, _("01 Month")),
        (TWO_MONTH, _("02 Months")),
        (THREE_MONTH, _("03 Months")),
        (FOUR_MONTH, _("04 Months")),
        (FIVE_MONTH, _("05 Months")),
        (SIX_MONTH, _("06 Months")),
    )    
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select category')
    # duration = forms.DateTimeField(input_formats=["%Y-%m-%dT%H:%M", ], widget=forms.Select(choices=PROPOSAL_DURATION))
    class Meta:
        model = Proposal
        fields = [
            'title', 'preview', 'category', 'description', 'sample_link', 'salary', 'service_level','revision', 'dura_converter', 'skill','faq_one','faq_one_description','thumbnail','video',
            'faq_two','faq_two_description','faq_three','faq_three_description','thumbnail','video', 'file_type'
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
        self.fields['video'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Embed Yourtube or Vimeo url'})
        self.fields['salary'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})            
        self.fields['service_level'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Specify level'})
        self.fields['revision'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Specify revision'})
        self.fields['dura_converter'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter dur.'})
        self.fields['file_type'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'file type'})
    


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




