from .models import Contractor, Contract, InternalContract
from teams.models import Team
from django.utils.translation import gettext_lazy as _
from django import forms
from proposals.models import Proposal


# a class to output datepicker on template
class DateInput(forms.DateInput):
    input_type = 'date'


class InternalContractForm(forms.ModelForm):
    proposal = forms.ModelChoiceField(queryset=InternalContract.objects.all(), empty_label='Select Proposal')

    class Meta:
        model = InternalContract
        fields = [
            'proposal','contract_duration', 'line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',
            'line_two','line_two_quantity', 'line_two_unit_price', 'line_two_total_price',
            'line_three','line_three_quantity', 'line_three_unit_price', 'line_three_total_price',
            'line_four','line_four_quantity', 'line_four_unit_price', 'line_four_total_price',
            'line_five','line_five_quantity', 'line_five_unit_price', 'line_five_total_price',
            'notes', 'grand_total'
        ] 

        required = [
         # Required details 
            'proposal', 'contract_duration', 'line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price','notes',               
        ]  
        readonly = [
            'line_one_total_price','line_two_total_price','line_three_total_price','line_four_total_price', 'line_five_total_price','grand_total',
        ]

    def __init__(self, team, *args, **kwargs):
        super(InternalContractForm, self).__init__(*args, **kwargs)        
        self.fields['proposal'].queryset = Proposal.active.filter(team=team)
       
        # 'Basic Info'
        self.fields['proposal'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Select proposal'})            
        self.fields['contract_duration'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Active Email'})
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
        # 'Product/Service #5',                    
        self.fields['line_five'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['line_five_quantity'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})            
        self.fields['line_five_unit_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})    
        self.fields['line_five_total_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})            
        self.fields['notes'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'notes'}) 
        # 'Grand Total',     
        self.fields['grand_total'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0}) 


        for field in self.Meta.required:
            self.fields[field].required = True

        for field in self.Meta.readonly:
            self.fields[field].widget.attrs["readonly"] = True



class ExternalContractForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Contract.objects.all(), empty_label='Select Contractor')

    class Meta:
        model = Contract
        fields = [
            'client', 'contract_duration', 'line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',
            'line_two','line_two_quantity', 'line_two_unit_price', 'line_two_total_price',
            'line_three','line_three_quantity', 'line_three_unit_price', 'line_three_total_price',
            'line_four','line_four_quantity', 'line_four_unit_price', 'line_four_total_price',
            'line_five','line_five_quantity', 'line_five_unit_price', 'line_five_total_price',
            'notes', 'grand_total'
        ] 

        required = [
         # Required details 
            'client', 'contract_duration', 'line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',               
        ]  

        readonly = [
            'line_one_total_price','line_two_total_price','line_three_total_price','line_four_total_price', 'line_five_total_price','grand_total',
        ]

    def __init__(self, team, *args, **kwargs):
        super(ExternalContractForm, self).__init__(*args, **kwargs)
        
        self.fields['client'].queryset = Contractor.objects.filter(team=team)
       
        # 'Basic Info'
        self.fields['client'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Full Name'})            
        self.fields['contract_duration'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Active Email'})
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
        # 'Product/Service #5',                    
        self.fields['line_five'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['line_five_quantity'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})            
        self.fields['line_five_unit_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})    
        self.fields['line_five_total_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0})            
        self.fields['notes'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'notes'}) 
        # 'Grand Total',     
        self.fields['grand_total'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 0}) 


        for field in self.Meta.required:
            self.fields[field].required = True


        for field in self.Meta.readonly:
            self.fields[field].widget.attrs["readonly"] = True


class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = ['name', 'email', 'address', 'postal_code','phone_Number',] 
        required = [
         # Required details 
            'name', 'email', 'address',               
        ]  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Full Name'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Active Email'})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Address of client'})                       
        self.fields['postal_code'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Postal Code'})
        self.fields['phone_Number'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Phone number'})            

     
        for field in self.Meta.required:
            self.fields[field].required = True


class ChangeContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = ['name', 'address', 'postal_code','phone_Number'] 


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Full Name'})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Address of client'})                       
        self.fields['postal_code'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Postal Code'})
        self.fields['phone_Number'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Phone number'})            

     




















