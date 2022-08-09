from django.contrib import admin
from .models import (Application)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['team', 'budget','project', 'created_at', 'message_slice', 'status']
    list_filter = ['team']
    readonly_fields = ('created_at',)
    search_fields = ['message']
    list_editable = ['status']
    radio_fields = {'status': admin.HORIZONTAL}       

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return True



admin.site.register(Application, ApplicationAdmin)