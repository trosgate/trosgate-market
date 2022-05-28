from argparse import Action
from faulthandler import disable
from django.contrib import admin
from .models import Package, Team, Invitation, TeamChat, AssignMember, Tracking

MAX_OBJECTS = 2


class PackageAdmin(admin.ModelAdmin):
    list_display = ['type','price', 'is_default', 'status', 'verbose_type', 'ordering']
    list_display_links = ['type','price']
    list_editable = ['verbose_type', 'ordering']
    readonly_fields = ['type']
    radio_fields = {'is_default': admin.HORIZONTAL}    


    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class TeamAdmin(admin.ModelAdmin):
    list_display = ['title','created_by', 'created_at', 'status', 'package_status', 'package']
    list_display_links = ['title', 'created_by']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'package']
    readonly_fields = ['stripe_customer_id','stripe_subscription_id','paypal_customer_id','paypal_subscription_id']

    fieldsets = (
        ('Introduction', {'fields': ('title', 'slug',)}),
        ('Background Details', {'fields': ('notice',)}),
        ('Team Manager', {'fields': ('created_by',)}),
        ('Team Member(s)', {'fields': ('members',)}),
        ('Package', {'fields': ('package','package_status', 'package_expiry',)}),
        ('Subscription Option #1', {'fields': ('stripe_customer_id','stripe_subscription_id',)}),
        ('Subscription Option #2', {'fields': ('paypal_customer_id','paypal_subscription_id',)}),
    )  
    radio_fields = {'status': admin.HORIZONTAL}

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class InvitationAdmin(admin.ModelAdmin):
    list_display = ['email','team', 'code', 'sent_on', 'status']
    list_display_links = ['email', 'team']
    list_editable = ['status']
    search_fields = ['code','email']
    list_filter = ['status']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class TeamChatAdmin(admin.ModelAdmin):
    list_display = ['team', 'sender','sent_on','content',]
    list_display_links = ['team']
    search_fields = ['team']
    list_filter = ['team']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class AssignMemberAdmin(admin.ModelAdmin):
    list_display = ['team', 'assignor','assignee', 'status', 'proposal','is_assigned']
    list_display_links = ['team']
    list_editable = ['is_assigned']
    search_fields = ['team__title']
    list_filter = ['team']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class TrackingAdmin(admin.ModelAdmin):
    list_display = ['team', 'assigned','created_by', 'tasks', 'is_tracked',]
    list_display_links = ['team']
    search_fields = ['team__title', 'tasks']
    list_filter = ['team']


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Team, TeamAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(TeamChat, TeamChatAdmin)
admin.site.register(AssignMember, AssignMemberAdmin)
admin.site.register(Tracking, TrackingAdmin)

