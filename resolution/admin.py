from django.contrib import admin
from .models import ProjectResolution, ApplicationReview, ProjectCompletionFiles



class ProjectResolutionAdmin(admin.ModelAdmin):
    model = ProjectResolution
    list_display = ['team', 'application', 'start_time', 'end_time']    
    # list_filter = ['purchase__status']


admin.site.register(ProjectResolution, ProjectResolutionAdmin)
admin.site.register(ApplicationReview)
admin.site.register(ProjectCompletionFiles)