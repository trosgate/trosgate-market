from django.contrib import admin
from . models import Client, ClientAccount, ClientAction


MAX_OBJECTS = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ['user', 'merchant', 'gender', 'tagline', 'image_tag']
    list_display_links = ['user', 'gender',]
    readonly_fields = [
        'gender', 'merchant', 'address','profile_photo', 'image_tag', 'banner_photo',  'banner_tag', 'company_logo', 'logo_tag',
        'employees', 'announcement','brand_name', 'tagline', 'description', 'business_size'
        ]
    search_fields = ['user__short_name', 'gender', 'tagline']
    fieldsets = (
        ('Personal info', {'fields': ('merchant', 'gender', 'address','profile_photo', 'image_tag', 'banner_photo',  'banner_tag', 'company_logo', 'logo_tag')}),
        ('Emploees', {'fields': ('employees', 'announcement',)}),
        ('Brand and Description', {'fields': ('brand_name', 'tagline', 'description', 'business_size', 'department',)}),
    )

    radio_fields = {'gender': admin.HORIZONTAL}

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super(ClientAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.all()  
        else:
            return qs.filter(pk=0)


@admin.register(ClientAccount)
class ClientAccountAdmin(admin.ModelAdmin):
    model = ClientAccount
    list_display = ['id', 'user', 'merchant', 'created_at', 'modified_on', 'available_balance']
    list_display_links = ['user', 'merchant',]
    readonly_fields = ['user', 'merchant', 'created_at', 'modified_on', 'debug_balance'] #, 'available_balance'
    exclude = ('debug_balance',)
    search_fields = ['id', 'user__short_name']

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
    readonly_fields = ['merchant', 'account','reference', 'gateway', 'narration', 'created_at', 'amount', 'deposit_fee', 'status']
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

