from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django import forms
from .models import Ticket, TicketMessage



class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'content', 'query_type', 'product_type', 'product_type_reference']
        required = ['title', 'content', 'query_type']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})

        self.fields['content'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})

        self.fields['query_type'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})
        
        self.fields['product_type'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})
        
        self.fields['product_type_reference'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})

        
        for field in self.Meta.required:
            self.fields[field].required = True


class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['content','link_title_one','link_title_one_backlink','link_title_two','link_title_two_backlink']
        required = ['content']
        readonly = ['content', 'link_title_one','link_title_one_backlink','link_title_two','link_title_two_backlink']
        disabled = ['content', 'link_title_one','link_title_one_backlink','link_title_two','link_title_two_backlink']
        widgets = {
            'content': forms.Textarea(attrs={'rows':10, 'cols':100}),
            'link_title_one': forms.Textarea(attrs={'rows':1, 'cols':100}),
            'link_title_two': forms.Textarea(attrs={'rows':1, 'cols':100}),
        }
        

    def __init__(self, *args, **kwargs):
        super(TicketMessageForm, self).__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

        for field in self.Meta.disabled:
            if self.instance.pk:
                self.fields[field].widget.attrs["disabled"] = True

        for field in self.Meta.readonly:
            if self.instance.pk:
                self.fields[field].widget.attrs["readonly"] = True


class TicketStatesForm(forms.ModelForm):
    ACTIVE = 'active'
    CLOSED = 'closed'
    STATUS = (
        (ACTIVE, 'Active'),
        (CLOSED, 'Close'),
    )
    states = forms.ChoiceField(required=True, choices=STATUS, label="Select Status")
    
    class Meta:
        model = Ticket
        fields = ['states']
        required = ['states']

    def __init__(self, *args, **kwargs):
        super(TicketStatesForm, self).__init__(*args, **kwargs)

        self.fields['states'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})

        for field in self.Meta.required:
            self.fields[field].required = True


class CustomerTicketReplyForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['content']
        required = ['content']

    def __init__(self, *args, **kwargs):
        super(CustomerTicketReplyForm, self).__init__(*args, **kwargs)

        self.fields['content'].widget.attrs.update(
            {'class': 'form-control col-12 float-left', 'placeholder': ''})

        for field in self.Meta.required:
            self.fields[field].required = True











































































































