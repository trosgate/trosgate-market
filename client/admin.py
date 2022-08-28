from django.contrib import admin
from . models import Client, ClientAccount, ClientAction


MAX_OBJECTS = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ['user', 'gender','budget_per_hourly_rate', 'tagline', 'image_tag']
    list_display_links = ['user', 'gender',]
    readonly_fields = ['image_tag', 'banner_tag', 'logo_tag']
    search_fields = ['user__short_name', 'gender', 'tagline']
    fieldsets = (
        ('Personal info', {'fields': ('gender', 'budget_per_hourly_rate', 'address','profile_photo', 'image_tag', 'banner_photo',  'banner_tag', 'company_logo', 'logo_tag')}),
        ('Emploees', {'fields': ('employees', 'announcement',)}),
        ('Brand and Description', {'fields': ('brand_name', 'tagline', 'description', 'business_size')}),
    )

    radio_fields = {'gender': admin.HORIZONTAL}

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ClientAccount)
class ClientAccountAdmin(admin.ModelAdmin):
    model = ClientAccount
    list_display = ['user', 'created_at', 'modified_on', 'available_balance']
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


@admin.register(ClientAction)
class ClientActionAdmin(admin.ModelAdmin):
    model = ClientAction
    list_display = ['account', 'reference', 'gateway', 'created_at', 'amount', 'deposit_fee', 'status']
    readonly_fields = ['account','reference', 'gateway', 'narration', 'created_at', 'amount', 'deposit_fee', 'status']
    search_fields = ['account__user__first_name', 'account__user__last_name', 'reference', 'gateway']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

