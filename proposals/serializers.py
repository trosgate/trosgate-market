from rest_framework import serializers
from django import forms
from general_settings.models import Skill, Category
from .models import Proposal


# category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), empty_label='Select category')   
class ProposalStepOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ['title', 'preview', 'category','skill', 'thumbnail']
        required = ['title', 'preview', 'category','skill', 'thumbnail']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].style['class'] = 'form-control'

        # self.fields['title'].widget.attrs.update(
        #     {'class': 'form-control', 'placeholder': 'Proposal Title'})
        # self.fields['preview'].widget.attrs.update(
        #     {'class': 'form-control', 'placeholder': 'Proposal Preview'})
        # self.fields['category'].widget.attrs.update(
        #     {'class': 'form-control', 'placeholder': 'Proposal Category'})        
        # self.fields['skill'].widget.attrs.update(
        #     {'class': 'form-control chosen-select Skills', 'placeholder': 'select some skills'})
        # self.fields['thumbnail'].widget.attrs.update(
        #     {'class': 'form-control', 'placeholder': ''})
        
        for field in self.Meta.required:
            self.fields[field].required = True

    def clean_skill(self):
        skill_count = self.cleaned_data['skill']
        if len(skill_count) > 3:
            raise forms.ValidationError(_("Skill selected must not be more than three"))
        return skill_count
    

# THE FIRST STEP WILL INHERIT FROM serializers.Serializer AND not serializers.ModelSerializer
class ProposalStepTwoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proposal
        fields = ['description', 'sample_link']
        required = ['description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal description'})
        self.fields['sample_link'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Proposal sample_link'})


class ProposalStepThreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proposal
        fields = ['faq_one','faq_one_description','faq_two','faq_two_description','faq_three','faq_three_description']
        required = ['faq_one','faq_one_description','faq_two','faq_two_description','faq_three','faq_three_description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faq_one'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #1 Question'})
        self.fields['faq_one_description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #1 Answer'})
        self.fields['faq_two'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #2 Question'})
        self.fields['faq_two_description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #2 Answer'})
        self.fields['faq_three'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #3 Question'})
        self.fields['faq_three_description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'FAQ #3 Answer'})

        for field in self.Meta.required:
            self.fields[field].required = True




