from django.contrib import admin
from . models import (
    OneClickResolution, ProjectResolution, ApplicationReview, 
    ProjectCompletionFiles, ProposalResolution,OneClickReview, 
    ProposalCompletionFiles, ProposalReview, ContractResolution, ContractReview
)


@admin.register(OneClickResolution)
class OneClickResolutionAdmin(admin.ModelAdmin):
    model = OneClickResolution
    list_display = ['team','start_time', 'end_time', 'status']    


@admin.register(OneClickReview)
class OneClickReviewAdmin(admin.ModelAdmin):
    model = OneClickReview
    list_display = ['title', 'resolution', 'rating','status']
    list_display_links = ['title']
    list_editable = [ 'status','rating']
    search_fields = ['title', 'resolution__team__title']


@admin.register(ProjectResolution)
class ProjectResolutionAdmin(admin.ModelAdmin):
    model = ProjectResolution
    list_display = ['team', 'application', 'start_time', 'end_time']    


@admin.register(ProjectCompletionFiles)
class ProjectResolutionFilesAdmin(admin.ModelAdmin):
    model = ProjectCompletionFiles
    list_display = ['application', 'attachment',]


@admin.register(ApplicationReview)
class ApplicationReviewAdmin(admin.ModelAdmin):
    model = ApplicationReview
    list_display = ['title', 'resolution', 'rating','status']
    list_display_links = ['title']
    list_editable = [ 'status','rating']
    search_fields = ['title', 'resolution__team__title']


@admin.register(ProposalResolution)
class ProposalResolutionAdmin(admin.ModelAdmin):
    model = ProposalResolution
    list_display = ['team','start_time', 'end_time', 'status']
    readonly_fields = ['team','start_time', 'end_time', 'status', 'proposal_sale']    


@admin.register(ProposalCompletionFiles)
class ProposalCompletionFilesAdmin(admin.ModelAdmin):
    model = ProposalCompletionFiles
    list_display = ['proposal', 'attachment']


@admin.register(ProposalReview)
class ProposalReviewAdmin(admin.ModelAdmin):
    model = ProposalReview
    list_display = ['title', 'resolution', 'rating', 'status']
    list_display_links = ['title']
    list_editable = [ 'status', 'rating']
    search_fields = ['title']


@admin.register(ContractResolution)
class ContractResolutionAdmin(admin.ModelAdmin):
    model = ContractResolution
    list_display = ['team','start_time', 'end_time', 'status'] 


@admin.register(ContractReview)
class ProposalReviewAdmin(admin.ModelAdmin):
    model = ContractReview
    list_display = ['title', 'resolution', 'rating', 'status']
    list_display_links = ['title']
    list_editable = [ 'status', 'rating']
    search_fields = ['title']