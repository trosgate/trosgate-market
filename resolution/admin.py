from django.contrib import admin
from .models import ProjectResolution, ProjectResolutionReview, ProjectCompletionFiles



class ProjectResolutionAdmin(admin.ModelAdmin):
    model = ProjectResolution
    list_display = ['team', 'application', 'start_time', 'end_time']    
    # list_filter = ['purchase__status']


admin.site.register(ProjectResolution, ProjectResolutionAdmin)
admin.site.register(ProjectResolutionReview)
admin.site.register(ProjectCompletionFiles)