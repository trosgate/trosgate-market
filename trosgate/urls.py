from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
# from two_factor.urls import urlpatterns as tf_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(tf_urls)),
    path('', include('account.urls', namespace='account')),
    path('client/', include('client.urls', namespace='client')),
    path('freelancer/', include('freelancer.urls', namespace='freelancer')), 
    path('project/', include('projects.urls', namespace='projects')),
    path('proposal/', include('proposals.urls', namespace='proposals')),
    path('team/', include('teams.urls', namespace='teams')),   
    path('category/', include('general_settings.urls', namespace='generalsettings')),
    path('notification/', include('notification.urls', namespace='notification')),
    path('application/', include('applications.urls', namespace='applications')),
    path('transaction/', include('transactions.urls', namespace='transactions')),
    path('contract/', include('contract.urls', namespace='contract')),
    path('project/quiz/', include('quiz.urls', namespace='quiz')),
    path('team/analytics/', include('analytics.urls', namespace='analytics')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('marketing/', include('marketing.urls', namespace='marketing')),
    path('manager/', include('resolution.urls', namespace='resolution')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Trosgate Admin"
admin.site.site_title = "Trosgate Admin Portal"
admin.site.index_title = "Welcome to Trosgate"