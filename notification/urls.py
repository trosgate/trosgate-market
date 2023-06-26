from django.urls import path, re_path
from . import views

app_name = 'notification'


urlpatterns = [
    path('chatroom/', views.chatroom, name='chatroom'),
    path('remove-chatroom/', views.remove_chatroom, name='remove_chatroom'),
    path('create-room/<str:room_name>/', views.create_room, name='create_room'),
    path('ws/<str:room_name>/', views.support_chatroom, name='support_chatroom'),
]