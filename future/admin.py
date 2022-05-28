from django.contrib import admin
from .models import FutureRelease

MAX_OBJECTS = 1

class FutureReleaseAdmin(admin.ModelAdmin):
    model = FutureRelease
    list_display = ['preview', 'alert']
    list_display_links = ['preview', 'alert']
    readonly_fields = ['preview', 'alert']

    fieldsets = (
    	('Know this before you launch features', {'fields': ('alert',)}),
        ('#1-Transfer/Gift Feature', {'fields': ('transfer',)}),
        ('Client Deposit Feature', {'fields': ('deposit',)}),                 
        ('More Teams Per Freelancer Feature', {'fields': ('more_team_per_user',)}),
        ('Freelancer External client Feature', {'fields': ('ext_contract',)}),
        ('Two Factor Authenticator(Twilio SMS)', {'fields': ('sms_authenticator',)}),       
    )

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

admin.site.register(FutureRelease, FutureReleaseAdmin)