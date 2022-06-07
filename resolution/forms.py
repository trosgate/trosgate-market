from .models import ProjectCompletionFiles
from django import forms


class ProjectCompletionForm(forms.ModelForm):
    #this works if you want boolean as radio buttons
    # completed = forms.TypedChoiceField(choices=[(True, 'Completed'), (False, 'Pending')], widget=forms.RadioSelect, coerce=bool)

    class Meta:
        model = ProjectCompletionFiles
        fields = ['attachment'] 


    def __init__(self, *args, **kwargs):
        super(ProjectCompletionForm, self).__init__(*args, **kwargs)
        
        # 'Basic Info'
        self.fields['attachment'].widget.attrs.update(
            {'class': 'form-control'})

