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
from django.utils.text import slugify
from notification.mailer import new_user_registration
from contract.models import Contract
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404


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


class CustomerRegisterForm(forms.ModelForm):
    FREELANCER = 'freelancer'
    CLIENT = 'client'
    USER_TYPE = (
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

        self.fields['short_name'].widget.attrs.update(
            {'class': 'input-group col-lg-12'})
        self.fields['email'].widget.attrs.update(
            {'class': 'input-group col-lg-12',})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'input-group col-lg-12',})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'input-group col-lg-12',})
        self.fields['phone'].widget.attrs.update(
            {'class': 'input-group col-lg-12',})
        self.fields['user_type'].widget.attrs.update(
            {'class': 'input-group col-lg-12',})
        self.fields['country'].widget.attrs.update(
            {'class': 'input-group col-lg-12',})
        self.fields['password1'].widget.attrs.update(
            {'class': 'input-group col-lg-12',})
        self.fields['password2'].widget.attrs.update(
            {'class': 'input-group col-lg-12',})

        for field in self.Meta.required:
            self.fields[field].required = True

    def clean_short_name(self):
        short_name = self.cleaned_data['short_name'].lower()
        a = Customer.objects.filter(short_name__icontains=short_name)
        if a.count():
            raise forms.ValidationError(_("Username already exists"))
        return short_name


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
        user.email = self.cleaned_data.get('email')
        user.short_name = self.cleaned_data.get('short_name')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone = self.cleaned_data.get('phone')
        user.country = self.cleaned_data.get('country')
        user.user_type = self.cleaned_data.get('user_type')
        user.set_password(self.cleaned_data["password1"])
        user.site = Site.objects.get_current()
        user.is_active = False
        user.save()

        if user.user_type == Customer.FREELANCER:
            
            FreelancerAccount.objects.get_or_create(user=user)[0]
            PaymentAccount.objects.get_or_create(user=user)[0]

            package = Package.objects.get_or_create(pk=1, type='Basic')[0]

            team = Team.objects.get_or_create(
                title=user.short_name,
                notice="This is the basic team", 
                created_by = user,
                package = package,
                package_status = Team.DEFAULT,
                slug = slugify(user.short_name)
            )[0]
            team.save()
            team.members.add(user)
            
            freelancer = Freelancer.objects.get_or_create(user=user)[0]
            freelancer.active_team_id = team.id
            freelancer.save()

            Invitation.objects.get_or_create(
                team=team, sender=user, email=user.email, 
                type=Invitation.INTERNAL,
            )[0]

        if user.user_type == Customer.CLIENT:
            Client.objects.get_or_create(user=user)[0]
            ClientAccount.objects.get_or_create(user=user)[0]
            
        db_transaction.on_commit(lambda: new_user_registration(user, user.email))

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
            {'class': 'input-group col-lg-12',})
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
        package = int(self.cleaned_data['package'])
        selected_package = get_object_or_404(Package, pk=package)

        user = Customer.objects.create_merchant(
            email=self.cleaned_data.get('email'), 
            business_name = self.cleaned_data.get("business_name"),
            password = self.cleaned_data.get("password1"),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'), 
            country = self.cleaned_data.get('country'),
            package=selected_package
        )
        db_transaction.on_commit(lambda: new_user_registration(user, user.email))

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