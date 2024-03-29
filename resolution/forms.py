from django import forms
from transactions.models import ProposalSale
# (
#     # ProjectCompletionFiles, 
#     # ApplicationCancellation,
#     ProposalSale
#     # ContractCancellation,
# )



class ProposalCancellationForm(forms.ModelForm):

    class Meta:
        model = ProposalSale
        fields = ['cancel_type', 'cancel_message']

    def __init__(self, *args, **kwargs):
        super(ProposalCancellationForm, self).__init__(*args, **kwargs)
        
        self.fields['cancel_type'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['cancel_message'].widget.attrs.update(
            {'class': 'form-control'})


# class ProjectCompletionForm(forms.ModelForm):
#     class Meta:
#         model = ProjectCompletionFiles
#         fields = ['attachment'] 

#     def __init__(self, *args, **kwargs):
#         super(ProjectCompletionForm, self).__init__(*args, **kwargs)
        
#         self.fields['attachment'].widget.attrs.update(
#             {'class': 'form-control'})


# class ApplicationCancellationForm(forms.ModelForm):

#     class Meta:
#         model = ApplicationCancellation
#         fields = ['cancel_type', 'message']

#     def __init__(self, *args, **kwargs):
#         super(ApplicationCancellationForm, self).__init__(*args, **kwargs)
        
#         self.fields['cancel_type'].widget.attrs.update(
#             {'class': 'form-control'})
#         self.fields['message'].widget.attrs.update(
#             {'class': 'form-control'})


# class ProposalCompletionForm(forms.ModelForm):
#     class Meta:
#         model = ProposalCompletionFiles
#         fields = ['attachment'] 

#     def __init__(self, *args, **kwargs):
#         super(ProposalCompletionForm, self).__init__(*args, **kwargs)
        
#         # 'Basic Info'
#         self.fields['attachment'].widget.attrs.update(
#             {'class': 'form-control'})



# class ContractCompletionForm(forms.ModelForm):

#     class Meta:
#         model = ProposalCompletionFiles
#         fields = ['attachment'] 


#     def __init__(self, *args, **kwargs):
#         super(ContractCompletionForm, self).__init__(*args, **kwargs)
        
#         # 'Basic Info'
#         self.fields['attachment'].widget.attrs.update(
#             {'class': 'form-control'})


# class ContractCancellationForm(forms.ModelForm):

#     class Meta:
#         model = ContractCancellation
#         fields = ['cancel_type', 'message']

#     def __init__(self, *args, **kwargs):
#         super(ContractCancellationForm, self).__init__(*args, **kwargs)
        
#         self.fields['cancel_type'].widget.attrs.update(
#             {'class': 'form-control'})
#         self.fields['message'].widget.attrs.update(
#             {'class': 'form-control'})

