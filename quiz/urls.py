
from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [

    #Urls for quiz table
    path('', views.list_quiz, name='list_quiz'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('participants/', views.quiz_participants, name='participants'),
    path('modify/<slug:quiz_slug>/', views.modify_quiz, name='modify_quiz'),
    path('detail/<slug:quiz_slug>/', views.quiz_detail, name='quiz_detail'),
    path('questions/<slug:quiz_slug>/', views.questions, name='questions'),
    path('take-test/<slug:quiz_slug>/', views.take_test, name='take_test'),
    path('select/<int:quiz_id>/', views.select_answers, name='quiz_result'),
    path('result-detail/<slug:quiz_slug>/', views.question_detail, name='question_detail'),
    path('my-participants/<slug:quiz_slug>/', views.quiz_participants, name='quiz_participants'),

]


