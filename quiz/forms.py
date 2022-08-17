from django.core.exceptions import ValidationError
from .models import Answer, Question, Quizes, Participant, Attempt
from django import forms
from general_settings.models import Skill
from projects.models import Project


# a class to output datepicker on template
class DateInput(forms.DateInput):
    input_type = 'date'


class QuizForm(forms.ModelForm):
    # deadline = forms.DateField(widget=DateInput)
    # duration = forms.IntegerField(max_value=360, min_value=1)

    class Meta:
        model = Quizes
        fields = ['title','skills', 'instruction', 'attempts', 'duration'] 


    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'eg. Python devs'})
        self.fields['skills'].widget.attrs.update(
            {'class': 'form-control chosen-select Skills', 'placeholder': ''})
        self.fields['instruction'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Quiz instruction'})
        self.fields['attempts'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 1})
        self.fields['duration'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 10})


class QuestionForm(forms.ModelForm):
    question = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    marks = forms.IntegerField(max_value=100, min_value=1, required=True)

    class Meta:
        model = Question
        fields = ['question', 'marks'] 
        required = ['question', 'marks']  


class AnswerForm(forms.ModelForm):
    answer = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    is_correct = forms.BooleanField(required=True)


    class Meta:
        model = Answer
        fields = ['answer','is_correct']     
        required = ['answer','is_correct']  


class QuizChangeForm(forms.ModelForm):
    # is_published = forms.BooleanField(required=True)


    class Meta:
        model = Quizes
        fields = ['instruction', 'attempts', 'duration', 'is_published']     

    def __init__(self, *args, **kwargs):
        super(QuizChangeForm, self).__init__(*args, **kwargs)


        self.fields['instruction'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['attempts'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['is_published'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['duration'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})
        self.fields['is_published'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': ''})



# class QuizForm(forms.ModelForm):
#     project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label='Select your Project')
#     deadline = forms.DateField(widget=DateInput)
#     # duration = forms.IntegerField(max_value=360, min_value=1)

#     class Meta:
#         model = Quizes
#         fields = ['title','skills', 'project', 'instruction', 'attempts', 'duration', 'is_published'] 


#     def __init__(self, author, *args, **kwargs):
#         super(QuizForm, self).__init__(*args, **kwargs)
#         self.fields['project'].queryset = Project.objects.filter(created_by=author)


#         self.fields['title'].widget.attrs.update(
#             {'class': 'form-control', 'placeholder': 'eg. Python devs'})



# @login_required
# @user_is_client
# def create_quiz(request):
#     if request.method == 'POST':
#         quiz_form = QuizForm(request.user, request.POST)
#         if quiz_form.is_valid():
#             newquiz = quiz_form.save(commit=False)
#             newquiz.created_by = request.user
#             newquiz.save()
#             quiz_form.save_m2m()

#             messages.info(request, 'Quiz created successfuly')

#             return redirect('quiz:questions', quiz_slug=newquiz.slug)

#     else:
#         quiz_form = QuizForm(request.user)
    
#     context = {
# 	    'quiz_form':quiz_form,
# 	}
#     return render(request, 'quiz/create_quiz.html', context)














