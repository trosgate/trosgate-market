from django.contrib import admin
from . models import (
    ProjectResolution, ApplicationReview, 
    ProjectCompletionFiles, ProposalResolution, 
    ProposalCompletionFiles, ProposalReview
)


class ProjectResolutionAdmin(admin.ModelAdmin):
    model = ProjectResolution
    list_display = ['team', 'application', 'start_time', 'end_time']    


class ProjectResolutionFilesAdmin(admin.ModelAdmin):
    model = ProjectCompletionFiles
    list_display = ['application', 'attachment',]


class ApplicationReviewAdmin(admin.ModelAdmin):
    model = ApplicationReview
    list_display = ['resolution', 'title', 'rating','status']
    list_display_links = ['resolution']
    list_editable = [ 'status','rating']
    search_fields = ['title', 'resolution__team__title']


class ProposalResolutionAdmin(admin.ModelAdmin):
    model = ProposalResolution
    list_display = ['team', 'proposal_sale', 'start_time', 'end_time']    


class ProposalCompletionFilesAdmin(admin.ModelAdmin):
    model = ProposalCompletionFiles
    list_display = ['proposal', 'attachment',]


class ProposalReviewAdmin(admin.ModelAdmin):
    model = ProposalReview
    list_display = ['resolution', 'title', 'rating','status']
    list_display_links = ['title']
    list_editable = [ 'status','rating']
    search_fields = ['title', 'resolution__team__title']


admin.site.register(ProjectResolution, ProjectResolutionAdmin)
admin.site.register(ApplicationReview, ApplicationReviewAdmin)
admin.site.register(ProjectCompletionFiles, ProjectResolutionFilesAdmin)
admin.site.register(ProposalResolution, ProposalResolutionAdmin)
admin.site.register(ProposalCompletionFiles, ProposalCompletionFilesAdmin)
admin.site.register(ProposalReview, ProposalReviewAdmin)