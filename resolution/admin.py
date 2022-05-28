from django.contrib import admin
from .models import ProjectResolution



class ProjectResolutionAdmin(admin.ModelAdmin):
    model = ProjectResolution
    list_display = ['team', 'purchase', 'project', 'start_time', 'end_time']    
    # list_filter = ['purchase__status']


admin.site.register(ProjectResolution, ProjectResolutionAdmin)