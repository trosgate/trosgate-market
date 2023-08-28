from django.core.exceptions import ValidationError
from .models import Team, TeamMember, TeamChat, AssignMember
from django import forms
from django.forms import Textarea
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


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['earning_ratio', 'status', 'member', 'team']
        required = ['earning_ratio', 'status', 'member', 'team']

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['style'] = 'height: 40px; margin:0 auto;'
        self.fields['earning_ratio'].widget.attrs['style'] = 'height: 40px; margin:0 auto;'
        
        self.fields['status'].widget.attrs.update(
            {'class': 'form-control customs-select',})
        self.fields['earning_ratio'].widget.attrs.update(
            {'class': 'form-control',})
        
        for field in self.Meta.required:
            self.fields[field].required = True

    
    def clean(self):
        cleaned_data = super().clean()
        earning_ratio = cleaned_data.get('earning_ratio')

        if earning_ratio is None:
            raise forms.ValidationError("Earning ratio cannot be empty.")
            
        return cleaned_data


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


class TeamGalleryForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['gallery_link']

    def __init__(self, *args, **kwargs):
        super(TeamGalleryForm, self).__init__(*args, **kwargs)

        self.fields['gallery_link'].widget.attrs['class'] = 'form-control'










