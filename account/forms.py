# from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Customer, Country, TwoFactorAuth
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.forms import ModelForm
from django import forms
from datetime import datetime



class CustomerRegisterForm(forms.ModelForm):
    FREELANCER = 'freelancer'
    CLIENT = 'client'
    USER_TYPE = (
        (FREELANCER, _('Freelancer')),
        (CLIENT, _('Client')),
    )
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    user_type = forms.ChoiceField(required=True, choices=USER_TYPE, label="Select Type")
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label='Select Country')

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name',
                  'email', 'short_name', 'phone', 'country', 'user_type', 'password1', 'password2']    
        required = ['first_name', 'last_name','email', 'short_name', 'country', 'user_type', 'password1', 'password2']               


    def __init__(self, supported_country, *args, **kwargs):
        super(CustomerRegisterForm, self).__init__(*args, **kwargs)
        self.fields['country'].queryset = Country.objects.filter(id__in=supported_country)

        for field in self.Meta.required:
            self.fields[field].required = True


    def clean_short_name(self):
        short_name = self.cleaned_data['short_name'].lower()
        a = Customer.objects.filter(short_name=short_name)
        if a.count():
            raise forms.ValidationError(_("Username already exists"))
        return short_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('Oops! Email taken. Please try another Email'))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


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
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
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
    pass_code = forms.CharField(help_text = "Enter SMS verification code sent to your phone number")

    class Meta:
        model = TwoFactorAuth
        fields = ['pass_code']
          
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

         # Personal Details   
        self.fields['pass_code'].widget.attrs.update(
            {'class': 'form-control',})

