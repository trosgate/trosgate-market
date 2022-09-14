from django.contrib import admin
from .models import (Application)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['team', 'budget', 'created_at', 'message_slice', 'status']
    list_filter = ['status']
    readonly_fields = ('team', 'budget', 'created_at', 'project', 'status', 'message', 'estimated_duration', 'applied_by')
    search_fields = ['message']
    radio_fields = {'status': admin.HORIZONTAL}       

    def has_delete_permission(self, request, obj=None):
        return False
        
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
            return False

