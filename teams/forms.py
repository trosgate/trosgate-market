from django.core.exceptions import ValidationError
from .models import Team, Invitation, TeamChat, AssignMember
from django import forms
from proposals.models import Proposal
from account.models import Customer
from freelancer.models import Freelancer
from django.utils.translation import gettext_lazy as _

class TeamCreationForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['title','notice'] 


class TeamModifyForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['title','notice'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control col-xs-12 col-sm-12 col-md-12 col-lg-12 float-center'})

        self.fields['notice'].widget.attrs.update(
            {'class': 'form-control col-xs-12 col-sm-12 col-md-12 col-lg-12 float-center'})


class InvitationForm(forms.ModelForm):
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'enter email',}))    
    class Meta:
        model = Invitation
        fields = ['email'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update(
            {'class': 'form-control col-xs-12 col-sm-12 col-md-12 col-lg-6 float-center'})


class TeamChatForm(forms.ModelForm):
    content = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control col-xs-12 col-sm-12 col-md-12 col-lg-6 float-center', 'placeholder': 'send a message',}))

    class Meta:
        model = TeamChat
        fields = ['content'] 


class AssignForm(forms.ModelForm):
    assignee = forms.ModelChoiceField(queryset=AssignMember.objects.all(), empty_label='Select Team Member')

    class Meta:
        model = AssignMember
        fields = ['assignee', 'duty'] 


    def __init__(self, assignee, *args, **kwargs):
        super(AssignForm, self).__init__(*args, **kwargs)
        self.fields['assignee'].queryset = Customer.objects.filter(team_member__in=assignee)

        self.fields['assignee'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['duty'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'describe the main duty e.g marketing of this proposal'})














