from .models import Purchase
from django import forms


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