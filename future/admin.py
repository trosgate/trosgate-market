from django.contrib import admin
from .models import FutureRelease, PluginFeature, Plugin

MAX_OBJECTS = 1

@admin.register(FutureRelease)
class FutureReleaseAdmin(admin.ModelAdmin):
    list_display = ['preview', 'alert']
    list_display_links = ['preview', 'alert']
    readonly_fields = ['deposit','ext_contract','preview', 'alert']

    fieldsets = (
    	('Know this before you launch Plugin. Also, remember to save your changes', {'fields': ('alert',)}),
        ('#1 - Client Deposit Plugin', {'fields': ('deposit',)}),                 
        ('#2 - External Contract Plugin', {'fields': ('ext_contract',)}),
        ('#3 - Payment Splitter (Transfer) Plugin', {'fields': ('transfer',)}),
        ('#4 - Teams Builder Plus Plugin', {'fields': ('more_team_per_user',)}),
        ('#5 - Two Factor Authenticator(Email Alert Available)', {'fields': ('sms_authenticator',)}),       
    )

    def get_queryset(self, request):
        qs = super(FutureReleaseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.all()  
        else:
            return qs.filter(pk=0)


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


@admin.register(PluginFeature)
class PluginFeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'preview', 'ordering']
    list_editable = ['ordering']


@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'mode', 'price', 'ordering']
    list_editable = ['status', 'mode', 'ordering']
    prepopulated_fields ={'slug': ('name',)}
    # radio_fields = {
    #     'status': admin.HORIZONTAL,
    #     'mode': admin.HORIZONTAL,
    # }