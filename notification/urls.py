from django.urls import path, re_path
from . import views

app_name = 'notification'


urlpatterns = [
    path('create-room/<str:reference>/', views.create_room, name='create_room'),
    path('<str:room_name>/', views.chatroom, name='chatroom'),
]