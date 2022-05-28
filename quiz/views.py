from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm, AnswerForm, QuizChangeForm
from teams.models import Team
from projects.models import Project
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from account.permission import user_is_freelancer, user_is_client
from teams.models import Team
from django.utils.text import slugify
from django.contrib import auth, messages
from .models import Answer, Question, Quizes, Participant, Attempt
from account.models import Customer
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from datetime import datetime, timedelta


@login_required
@user_is_client
def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            newquiz = quiz_form.save(commit=False)
            newquiz.created_by = request.user
            newquiz.save()
            quiz_form.save_m2m()

            messages.info(request, 'Quiz created successfuly')

            return redirect('quiz:questions', quiz_slug=newquiz.slug)

    else:
        quiz_form = QuizForm()
    
    context = {
	    'quiz_form':quiz_form,
	}
    return render(request, 'quiz/create_quiz.html', context)


@login_required
def list_quiz(request):
    quiz_change_form = QuizChangeForm()
    if request.user.user_type == Customer.FREELANCER:
        quizz = Quizes.objects.filter(is_published=True)
    elif request.user.user_type == Customer.CLIENT:
        quizz = Quizes.objects.filter(created_by=request.user)
    
    context = {
	    'quizz':quizz,
	    'quiz_change_form':quiz_change_form,
	}
    return render(request, 'quiz/quizes_list.html', context)


@login_required
@user_is_client
def modify_quiz(request, quiz_slug):
    quiz = get_object_or_404(Quizes, slug=quiz_slug, created_by=request.user)

    quiz_change_form = QuizChangeForm(request.POST, instance=quiz)

    if request.method == 'POST':
        if quiz_change_form.is_valid():
            quiz_change_form.save()

            messages.info(request, 'Quiz modified successfuly')

            return redirect('quiz:list_quiz')

    quiz_change_form = QuizChangeForm(instance=quiz)
    context = {
	    'quiz':quiz,
	    'quiz_change_form':quiz_change_form,
	}
    return render(request, 'quiz/modify_quiz.html', context)


@login_required
@user_is_client
def questions(request, quiz_slug):
    quiz = get_object_or_404(Quizes, slug=quiz_slug, created_by=request.user)
    
    if not quiz:
        messages.info(request, 'You must start by creating a quiz')
        return redirect('quiz:create_quiz')
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            quest = question_form.cleaned_data.get('question')
            mark = question_form.cleaned_data.get('marks')
            answer = request.POST.getlist('answer')
            is_correct = request.POST.getlist('is_correct')

            messages.info(request, 'Question and answers added')
            question = Question.objects.create(question=quest, marks=mark, created_by=request.user)
            print(request.POST)
            print(answer, is_correct)

            for ans, cor in zip(answer, is_correct):
                new_answer = Answer.objects.create(answer=ans, is_correct=cor, created_by=request.user)

                question.answers.add(new_answer)
                question.save()
            
                quiz.questions.add(question)
                quiz.save()

            return redirect('quiz:questions', quiz_slug=quiz.slug)
    
    else:
        question_form = QuestionForm()
    
    context = {
	    'question_form':question_form,
	}
    return render(request, 'quiz/add_questions.html', context)


@login_required
def quiz_detail(request, quiz_slug):

    if request.user.user_type == Customer.FREELANCER:
        quiz = get_object_or_404(Quizes,  slug=quiz_slug, is_published=True)
        participant = quiz.participants.filter(participant = request.user)
        max_quiz_attempts = quiz.attempts
        participant_attempts = quiz.participants.filter(participant = request.user).count()

    elif request.user.user_type == Customer.CLIENT:
        quiz = get_object_or_404(Quizes,  slug=quiz_slug, created_by=request.user)
        participant = quiz.participants.all()
        max_quiz_attempts = quiz.attempts
        participant_attempts = quiz.participants.count()

        
    context = {
        'quiz': quiz,
        'max_quiz_attempts': max_quiz_attempts,
        'participant': participant,
        'participant_attempts': participant_attempts,
    }
    return render(request, 'quiz/quiz_detail.html', context)


@login_required
@user_is_freelancer
def take_test(request, quiz_slug):
    quiz = get_object_or_404(Quizes, slug=quiz_slug, is_published=True)

    time_duration = timedelta(minutes = quiz.duration) 
    time_remaining = (datetime.now() + time_duration)
    print(time_duration)
    print(datetime.now())
    print(time_remaining)
    
    context = {
        'quiz': quiz,
        'time_remaining': time_remaining,
    }
    return render(request, 'quiz/take_quiz.html', context)


@login_required
@user_is_freelancer
def select_answers(request, quiz_id):
    quiz = get_object_or_404(Quizes, pk=quiz_id, is_published=True)
    marks = 0

    if request.method == 'POST':
        question = request.POST.getlist('question')
        answer = request.POST.getlist('answer')
        participant = Participant.objects.create(participant = request.user, quiz=quiz, score=0)

        for ques, ans in zip(question, answer):
            question = Question.objects.get(id=ques)
            answer = Answer.objects.get(id=ans)
            Attempt.objects.create(quiz=quiz, participant=participant, question=question, answer=answer)
            if answer.is_correct == True:
                marks += question.marks
                participant.score += marks
                participant.save()

        messages.info(request, f'You have completed with a score of {marks}')

        return redirect('quiz:list_quiz')


def question_detail(request, quiz_slug):
    quiz = get_object_or_404(Quizes, slug=quiz_slug, created_by = request.user)
    questions = quiz.questions.all()
    participant = Attempt.objects.filter(quiz=quiz, participant__participant=request.user)

    context = {
        'quiz': quiz,
        'participant': participant,
        'questions': questions,

    }
    return render(request, 'quiz/question_detail.html', context)


@login_required
@user_is_client
def quiz_participants(request, quiz_slug):
    quiz = get_object_or_404(Quizes, slug=quiz_slug, is_published=True, created_by = request.user)
    participants = quiz.participants.all()

    context = {
        'quiz': quiz,
        'participants': participants,

    }
    return render(request, 'quiz/participant.html', context)
