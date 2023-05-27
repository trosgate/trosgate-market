
from django.urls import path
from . import views

app_name = 'projects'


urlpatterns = [
    #Urls for project table
    path('', views.project_list, name='project_list'),
    path('manage-projects', views.merchant_project, name='merchant_project'),
    path('create-project/', views.create_project, name='create_project'),
    path('active-projects/', views.active_project, name='active_project'),
    path('review-projects/', views.review_project, name='review_project'),
    path('archive-projects/', views.archived_project_view, name='archived_project_view'),

    # path('account/ongoing-projects/', views.ongoing_project, name='ongoing_project'),
    path('archive/<slug:project_slug>',views.archive_project, name='archive_project'),
    path('restore/<slug:project_slug>',views.restore_archive_project, name='restore_archive_project'),
    path('detail/<slug:project_slug>',views.project_single, name='project_detail'),
    path('<slug:project_slug>/reopen/', views.reopen_project, name='reopen_project'),
    path('delete-project/<int:pk>/',views.delete_project, name='delete_project'),

]
