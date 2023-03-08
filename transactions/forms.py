from .models import Purchase, ProposalSale, ApplicationSale, ContractSale, ExtContract, OneClickPurchase
from django import forms
from account.fund_exception import FundException
from django.utils.translation import gettext_lazy as _


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['full_name', 'email', 'phone'] 
        required = ['full_name', 'email', 'phone']  


    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        
        # 'Basic Info'
        self.fields['full_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter Full Name'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Active Email'})
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Address of client'}) 


        for field in self.Meta.required:
            self.fields[field].required = True


class BaseMemoForm(forms.Form):
    REFUND = 'refund'
    STATUS_CHOICES = (
        (REFUND, _('Refund Now')),
    )    
    status = forms.ChoiceField(required=True, choices=STATUS_CHOICES, label="Submit to Refund")
    
    def form_action(self, pk):

        if pk is None:
            raise FundException(_("Bad request. Try again later"))

    def save(self, pk):
        try:
            action = self.form_action(pk)
        except Exception as e:
            error_message = str(e)
            self.add_error(None, error_message)           
            raise
            
        return pk, action

class ProposalRefundForm(BaseMemoForm):
    def form_action(self, pk):
        return ProposalSale.proposal_refund(pk=pk)


class ApplicationRefundForm(BaseMemoForm):
    def form_action(self, pk):
        return ApplicationSale.application_refund(pk=pk)


class ContractRefundForm(BaseMemoForm):
    def form_action(self, pk):
        return ContractSale.contract_refund(pk=pk)

class ExtContractRefundForm(BaseMemoForm):
    def form_action(self, pk):
        return ExtContract.contract_refund(pk=pk)

class OneClickRefundForm(BaseMemoForm):
    def form_action(self, pk):
        return OneClickPurchase.oneclick_refund(pk=pk)


















































