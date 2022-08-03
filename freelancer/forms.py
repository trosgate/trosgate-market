from django.core.exceptions import ValidationError
from .models import Freelancer, FreelancerAction, FreelancerAccount
from general_settings.models import Department, Size
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.forms import ModelForm
from django import forms
from datetime import datetime
from account.models import Customer
from account.fund_exception import FundException
from notification.mailer import send_credit_to_team
from general_settings.fund_control import get_min_deposit, get_max_deposit
from teams.models import Team

class DateInput(forms.DateInput):
    input_type = 'date'


class FreelancerForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput, required=False)
    end_date = forms.DateField(widget=DateInput, required=False)
    start_date_two = forms.DateField(widget=DateInput, required=False)
    end_date_two = forms.DateField(widget=DateInput, required=False)
    profile_photo = forms.ImageField(widget=forms.FileInput,)
    banner_photo = forms.ImageField(widget=forms.FileInput,)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.RadioSelect)
    business_size = forms.ModelChoiceField(queryset=Size.objects.all(), widget=forms.RadioSelect)
    image_one = forms.ImageField(widget=forms.FileInput, required=False)
    image_two = forms.ImageField(widget=forms.FileInput, required=False)
    image_three = forms.ImageField(widget=forms.FileInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # personal details
        self.fields['gender'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Select Gender'})
        self.fields['hourly_rate'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Your Hourly Rate'})
        self.fields['tagline'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'tagline'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'description'})
        self.fields['brand_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'brand name'})
        self.fields['profile_photo'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'profile photo'})
        self.fields['banner_photo'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'banner photo'})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Country address'})
        self.fields['skill'].widget.attrs.update(
            {'class': 'form-control col-12', 'placeholder': 'User Skills'})
        #Education and Experience
        self.fields['company_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'company name'})
        self.fields['start_date'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'YYYY-MM-DD'})
        self.fields['end_date'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'YYYY-MM-DD'})
        self.fields['job_position'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Prev Job position'})
        self.fields['job_description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Prev Job description'})
        self.fields['company_name_two'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'company name'})
        self.fields['start_date_two'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'YYYY-MM-DD'})
        self.fields['end_date_two'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'YYYY-MM-DD'})
        self.fields['job_position_two'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Prev Job position'})
        self.fields['job_description_two'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Prev Job description'})
        # Projects and Awards
        self.fields['project_title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Award title'})
        self.fields['project_url'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'E.g. https: // example.com'})
        self.fields['project_title_two'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Award title'})
        self.fields['project_url_two'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'E.g. https: // example.com'})
        self.fields['project_title_three'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Award title'})
        self.fields['project_url_three'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'E.g. https: // example.com'})

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = Freelancer
        fields = [
            # personal details required
            'gender', 'hourly_rate', 'tagline', 'description', 'address', 'skill', 'profile_photo', 'banner_photo', 'brand_name', 'business_size', 'department',
            #Education and Experience
            'company_name', 'job_position', 'job_description', 'start_date', 'end_date', 'company_name_two', 'job_position_two', 'start_date_two', 'end_date_two', 'job_description_two',
            # Projects and Awards
            'project_title', 'project_url', 'image_one', 'project_title_two', 'project_url_two', 'image_two', 'project_title_three', 'project_url_three', 'image_three',
        ]

        required = [
            # Required details
            'gender', 'hourly_rate', 'tagline', 'description', 'address', 'skill', 'profile_photo', 'banner_photo', 'business_size', 'department',
        ]


class FundTransferForm(forms.ModelForm):

    team_staff = forms.ModelChoiceField(queryset=Freelancer.active.all(), empty_label='Select Receiver')

    class Meta:
        model = FreelancerAction
        fields = ['team_staff', 'debit_amount', 'position']
        required = ['debit_amount', 'position']

    def __init__(self, receiver, *args, **kwargs):
        super(FundTransferForm, self).__init__(*args, **kwargs)
        self.fields['team_staff'].queryset = Customer.objects.filter(team_member__in=receiver).exclude(teammanager__in=receiver)

        self.fields['team_staff'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})
        self.fields['debit_amount'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})
        self.fields['position'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})

        for field in self.Meta.required:
            self.fields[field].required = True


class WithdrawalForm(forms.ModelForm):

    class Meta:
        model = FreelancerAction
        fields = ['gateway', 'withdraw_amount', 'narration']
        required = ['gateway', 'withdraw_amount', 'narration']

    def __init__(self, *args, **kwargs):
        super(WithdrawalForm, self).__init__(*args, **kwargs)

        self.fields['gateway'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})

        self.fields['withdraw_amount'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})

        self.fields['narration'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})
        
        for field in self.Meta.required:
            self.fields[field].required = True


class BaseAccountForm(forms.Form):
    comment = forms.CharField(required=False, widget=forms.Textarea,)
    send_email = forms.BooleanField(required=False,)

    def form_action(self, account, user):
        
        if account == '':
            raise FundException(_("Bad request. Try again later"))

        if user == '':
            raise FundException(_("Bad request. Try again later"))

    def save(self, account, user):
        try:
            action = self.form_action(account, user)
        except Exception as e:
            error_message = str(e)
            self.add_error(None, error_message)           
            raise
        
        active_team = ''
        if self.cleaned_data.get('send_email', False):
            team = Team.objects.filter(created_by=account.user, status=Team.ACTIVE)
            if len(team) > 0:
                active_team = team.first()
            try:
                send_credit_to_team(account, active_team)
            except Exception as e:
                error_message = str(e)
                print(error_message)

        return account, action

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
class AdminCreditForm(BaseAccountForm):
    amount = forms.IntegerField(
        min_value=get_min_deposit(), 
        max_value=get_max_deposit(),
        required=True,
        help_text = 'How much to give out as credit'
    )
    field_order = ('amount', 'comment', 'send_email',)

    def form_action(self, account, user):
        return FreelancerAccount.admin_credit(
            account=account,
            user=user,
            amount = self.cleaned_data['amount'],
            comment = self.cleaned_data['comment'],
            created_at = timezone.now()
        )























































































































