from django.contrib import admin
from . models import (
    OneClickResolution, OneClickCancellation, ProjectResolution, ApplicationReview,
    ProjectCompletionFiles, ProposalResolution,OneClickReview, ApplicationCancellation,
    ProposalCompletionFiles, ProposalReview, ContractResolution,ContractCancellation, 
    ContractReview, ProposalCancellation,ApplicationCancellation
)


@admin.register(OneClickResolution)
class OneClickResolutionAdmin(admin.ModelAdmin):
    model = OneClickResolution
    list_display = ['team','start_time', 'end_time', 'status']    
    readonly_fields = ['team','start_time', 'end_time', 'status', 'oneclick_sale']


    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(OneClickCancellation)
class OneClickCancellationAdmin(admin.ModelAdmin):
    model = OneClickCancellation
    list_display = ['cancel_type', 'status', 'created_at', 'message']
    list_display_links = None


    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(OneClickReview)
class OneClickReviewAdmin(admin.ModelAdmin):
    model = OneClickReview
    list_display = ['resolution', 'title', 'rating', 'message']
    list_display_links = ['resolution','title']
    list_display_links = None
    search_fields = ['title', 'resolution__team__title', 'message']
    readonly_fields = ['title', 'resolution', 'rating','status','message']

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ProjectResolution)
class ProjectResolutionAdmin(admin.ModelAdmin):
    model = ProjectResolution
    list_display = ['team','start_time', 'end_time', 'status']    
    readonly_fields = ['team','start_time', 'end_time', 'status', 'application']


    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ProjectCompletionFiles)
class ProjectResolutionFilesAdmin(admin.ModelAdmin):
    model = ProjectCompletionFiles
    list_display = ['application', 'attachment',]


    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ApplicationCancellation)
class ApplicationCancellationAdmin(admin.ModelAdmin):
    model = ApplicationCancellation
    list_display = ['cancel_type', 'status', 'created_at', 'message']
    list_display_links = None

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ProposalCancellation)
class ProposalCancellationAdmin(admin.ModelAdmin):
    model = ProposalCancellation
    list_display = ['cancel_type', 'status', 'created_at', 'message']
    list_display_links = None

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ContractCancellation)
class ContractCancellationAdmin(admin.ModelAdmin):
    model = ContractCancellation
    list_display = ['cancel_type', 'status', 'created_at', 'message']
    list_display_links = None

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ApplicationReview)
class ApplicationReviewAdmin(admin.ModelAdmin):
    model = ApplicationReview
    list_display = ['resolution', 'title', 'rating', 'message']
    list_display_links = ['resolution','title']
    list_display_links = None
    search_fields = ['title', 'resolution__team__title', 'message']
    readonly_fields = ['title', 'resolution', 'rating','status','message']

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ProposalResolution)
class ProposalResolutionAdmin(admin.ModelAdmin):
    model = ProposalResolution
    list_display = ['team','start_time', 'end_time', 'status']
    readonly_fields = ['team','start_time', 'end_time', 'proposal_sale']    

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ProposalCompletionFiles)
class ProposalCompletionFilesAdmin(admin.ModelAdmin):
    model = ProposalCompletionFiles
    list_display = ['proposal', 'attachment']

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ProposalReview)
class ProposalReviewAdmin(admin.ModelAdmin):
    model = ProposalReview
    list_display = ['resolution', 'title', 'rating', 'message']
    list_display_links = ['resolution','title']
    list_display_links = None
    search_fields = ['title', 'resolution__team__title','message']
    readonly_fields = ['title', 'resolution', 'rating','status','message']

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ContractResolution)
class ContractResolutionAdmin(admin.ModelAdmin):
    model = ContractResolution
    list_display = ['team','start_time', 'end_time', 'status'] 

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ContractReview)
class ContractReviewAdmin(admin.ModelAdmin):
    model = ContractReview
    list_display = ['resolution', 'title', 'rating', 'message']
    list_display_links = ['resolution','title']
    list_display_links = None
    search_fields = ['title', 'resolution__team__title', 'message']
    readonly_fields = ['title', 'resolution', 'rating','status','message']

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions