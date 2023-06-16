from django.db import transaction as db_transaction
from django.core.exceptions import ValidationError
from . models import Customer, Country, Package, Merchant, TwoFactorAuth
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.forms import ModelForm
from django import forms
from datetime import datetime
from freelancer.models import Freelancer, FreelancerAccount
from payments.models import PaymentAccount
from client.models import Client, ClientAccount
from teams.models import Team, Invitation
from contract.models import Contract
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from .validators import DomainValidator, DomainField


class SearchTypeForm(forms.Form):
    WELCOME = 'welcome'
    FREELANCER = 'freelancer'
    PROPOSAL = 'proposal'
    USER_TYPE = (
        (WELCOME, _('Select search option')),
        (FREELANCER, _('Search Freelancer')),
        (PROPOSAL, _('Seaarch Proposal')),
    )
    search_type = forms.ChoiceField(choices=USER_TYPE, label="Select Type")

    def __init__(self, *args, **kwargs):
        super(SearchTypeForm, self).__init__(*args, **kwargs)

        self.fields['search_type'].widget.attrs.update(
            {'class': 'form-control'})


class MerchantthemeForm(forms.ModelForm):

    class Meta:
        model = Merchant
        fields = [
            'category_type', 'project_type', 'proposal_detail', 'banner_type', 'promo_type', 
        ]

    def __init__(self, *args, **kwargs):
        super(MerchantthemeForm, self).__init__(*args, **kwargs)

        self.fields['category_type'].widget.attrs['class'] = 'custom-select'
        self.fields['category_type'].widget.attrs['style'] = 'height: 40px;'

        self.fields['proposal_detail'].widget.attrs['class'] = 'custom-select'
        self.fields['proposal_detail'].widget.attrs['style'] = 'height: 40px;'

        self.fields['banner_type'].widget.attrs['class'] = 'custom-select'
        self.fields['banner_type'].widget.attrs['style'] = 'height: 40px;'

        self.fields['project_type'].widget.attrs['class'] = 'custom-select'
        self.fields['project_type'].widget.attrs['style'] = 'height: 40px;'

        self.fields['promo_type'].widget.attrs['class'] = 'custom-select'
        self.fields['promo_type'].widget.attrs['style'] = 'height: 40px;'


class MerchantBrandingForm(forms.ModelForm):

    class Meta:
        model = Merchant
        fields = [
            'title_block','subtitle_block','button_color', 'navbar_color',
            'tagline', 'description','announcement','footer_description',
        ]

    def __init__(self, *args, **kwargs):
        super(MerchantBrandingForm, self).__init__(*args, **kwargs)
        self.fields['title_block'].widget.attrs['class'] = 'custom-select'
        self.fields['title_block'].widget.attrs['style'] = 'height: 40px;'
        
        self.fields['tagline'].widget.attrs['class'] = 'custom-select'
        self.fields['tagline'].widget.attrs['style'] = 'height: 40px;'

        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['style'] = 'height: 150px;'

        self.fields['announcement'].widget.attrs['class'] = 'form-control'
        self.fields['announcement'].widget.attrs['style'] = 'height: 150px;'

        self.fields['button_color'].widget.attrs['class'] = 'custom-select'
        self.fields['button_color'].widget.attrs['style'] = 'height: 40px;'

        self.fields['navbar_color'].widget.attrs['class'] = 'custom-select'
        self.fields['navbar_color'].widget.attrs['style'] = 'height: 40px;'
        
        self.fields['subtitle_block'].widget.attrs.update(
            {'class': 'form-control',})

        self.fields['subtitle_block'].widget.attrs.update(
            {'class': 'form-control',})

        self.fields['footer_description'].widget.attrs['class'] = 'form-control'
        self.fields['footer_description'].widget.attrs['style'] = 'height: 150px;'


class CustomerRegisterForm(forms.ModelForm):
    SELECT_USER = 'User Type'
    FREELANCER = 'freelancer'
    CLIENT = 'client'
    USER_TYPE = (
        (SELECT_USER, _('Select User Type')),
        (FREELANCER, _('Freelancer')),
        (CLIENT, _('Client')),
    )
    short_name = forms.CharField(label='Username', min_length=4, max_length=30)
    email = forms.EmailField(label='Email', max_length=100)
    first_name = forms.CharField(label='First Name',  min_length=2, max_length=50)
    last_name = forms.CharField(label='Last Name', min_length=2, max_length=50)
    phone = forms.CharField(label='Phone', min_length=2, max_length=50)
    user_type = forms.ChoiceField(choices=USER_TYPE, label="Select Type")
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label='Select Country')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name','email', 'short_name', 'phone', 'country', 'user_type', 'password1', 'password2']    
        required = ['first_name', 'last_name','email', 'short_name', 'phone', 'country', 'user_type', 'password1', 'password2']               


    def __init__(self, supported_country, *args, **kwargs):
        super(CustomerRegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['country'].queryset = Country.objects.filter(id__in=supported_country)
        self.fields['country'].widget.attrs['class'] = 'custom-select'
        self.fields['country'].widget.attrs['style'] = 'height: 40px;'

        self.fields['user_type'].widget.attrs['class'] = 'custom-select'
        self.fields['user_type'].widget.attrs['style'] = 'height: 40px;'
        
        self.fields['short_name'].widget.attrs['class'] = 'form-control'
        self.fields['short_name'].widget.attrs['style'] = 'height: 40px;'
        
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['style'] = 'height: 40px;'
        
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['style'] = 'height: 40px;'
        
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['style'] = 'height: 40px;'
        
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['style'] = 'height: 40px;'
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['style'] = 'height: 40px;'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['style'] = 'height: 40px;'
        
        for field in self.Meta.required:
            self.fields[field].required = True


    def clean_short_name(self):
        short_name = self.cleaned_data['short_name'].lower()
        a = Customer.objects.filter(short_name__isnull=True, short_name__iexact=short_name)
        if a.count():
            raise forms.ValidationError(_("Username already exists"))
        return short_name


    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Oops! Email taken. Please try another Email"))

        if not email.islower():
            raise forms.ValidationError(_("Email characters must all be in lowercase"))
        return email


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


    @db_transaction.atomic
    def save(self):
        user = super().save(commit=False)
        try:
            Customer.objects.create_merchant_user(
                email=self.cleaned_data.get('email'), 
                first_name = self.cleaned_data.get("first_name"),
                last_name = self.cleaned_data.get('last_name'), 
                short_name = self.cleaned_data.get('short_name'),
                country = self.cleaned_data.get('country'),
                user_type = self.cleaned_data.get('user_type'),
                phone = self.cleaned_data.get('phone'),
                password = self.cleaned_data.get("password1"),
            )

        except Exception as e:
            error = str(e)
            raise ValidationError(f"{error}")

        return user


class MerchantRegisterForm(forms.ModelForm):
    business_name = forms.CharField(label='Business name', min_length=4, max_length=30)
    email = forms.EmailField(label='Email', max_length=100)
    first_name = forms.CharField(label='First Name',  min_length=2, max_length=50)
    last_name = forms.CharField(label='Last Name', min_length=2, max_length=50)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label='Select Business Country')
    package = forms.IntegerField()
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name','email', 'phone', 'country', 'business_name', 'package', 'password1', 'password2']    
        required = ['first_name', 'last_name','email', 'phone', 'country', 'business_name', 'password1', 'password2']               


    def __init__(self, supported_country, *args, **kwargs):
        super(MerchantRegisterForm, self).__init__(*args, **kwargs)
        self.fields['country'].queryset = Country.objects.filter(id__in=supported_country)

        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control',})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control',})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control',})
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control',})
        self.fields['country'].widget.attrs.update(
            {'class': 'form-control',})
        self.fields['business_name'].widget.attrs.update(
            {'class': 'form-control',})
        self.fields['package'].widget.attrs.update(
            {'class': 'form-control',})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control',})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control',})

        for field in self.Meta.required:
            self.fields[field].required = True


    def clean_business_name(self):
        business_name = self.cleaned_data['business_name'].lower()
        a = Merchant.objects.filter(business_name__iexact=business_name)
        if a.count():
            raise forms.ValidationError(_("Business name already taken"))
        return business_name


    def clean_country(self):
        country = self.cleaned_data['country']
        if not country:
            raise forms.ValidationError(_("Country of business required"))
        return country


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone:
            raise forms.ValidationError(_("Phone number required"))
        return phone


    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email__icontains=email).exists():
            raise forms.ValidationError(_("Oops! Email taken. Please try another Email"))

        if not email.islower():
            raise forms.ValidationError(_("Email characters must all be in lowercase"))
        return email


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


    @db_transaction.atomic
    def save(self):
        user = super().save(commit=False)
        try:
            selected_package = Package.objects.get(pk=int(self.cleaned_data['package']))
            Customer.objects.create_merchant(
                email=self.cleaned_data.get('email'), 
                business_name = self.cleaned_data.get("business_name"),
                password = self.cleaned_data.get("password1"),
                first_name = self.cleaned_data.get('first_name'),
                last_name = self.cleaned_data.get('last_name'), 
                country = self.cleaned_data.get('country'),
                package=selected_package
            )
        except Exception as e:
            error = str(e)
            raise ValidationError(f"{error}")

        return user


class UserLoginForm(AuthenticationForm):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Email Address',
               'id': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        curr_site = Site.objects.get_current()
        cust_email = Customer.objects.filter(curr_site=curr_site, email=email).exists()
        if not cust_email:
            raise ValidationError('Ooops! the input detail(s) is not valid')
        return email


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        cust_email = Customer.objects.filter(email=email)
        if not cust_email:
            raise forms.ValidationError(
                'Ooops! the input detail(s) is not valid')
        return email


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class TwoFactorAuthForm(forms.ModelForm): 
    pass_code = forms.CharField(help_text = "Enter verification token sent to your email")

    class Meta:
        model = TwoFactorAuth
        fields = ['pass_code']
          
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

         # Personal Details
        self.fields['pass_code'].widget.attrs.update(
            {'class': 'form-control',})

    def clean_passcode(self):
        pass_code = self.cleaned_data['pass_code']
        checker = TwoFactorAuth.objects.filter(pass_code=pass_code)

        if not checker:    
            raise forms.ValidationError(
                _('Invalid token entered. Please check and try again'))
        return pass_code


class DomainForm(forms.Form): 
    domain = DomainField(error_messages={'invalid': 'Please enter a valid domain name.'})

    def __init__(self, *args, **kwargs):
        super(DomainForm, self).__init__(*args, **kwargs)
        self.fields['domain'].widget.attrs['class'] = 'form-control col-12 col-sm-12 col-md-12 col-lg-12'

    
    def clean_domain(self):
        domain = self.cleaned_data['domain'].lower()
        validator = DomainValidator(domain)
        if not validator.validate():
            raise ValidationError('connection denied for provided domain')

        return domain
    



