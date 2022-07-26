from django.contrib import admin
from .models import PaymentAccount, PaymentRequest


class PaymentAccountAdmin(admin.ModelAdmin):
    model = PaymentAccount
    list_display = ['user', 'created_at']
    readonly_fields = ['user','created_at',]
    list_display_links = ['user',]


    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class PaymentRequestAdmin(admin.ModelAdmin):
    model = PaymentRequest
    list_display = ['user', 'team', 'gateway', 'amount', 'status_choice', 'created_at', 'payday']
    readonly_fields = ['user','created_at', 'payday']
    list_display_links = ['user','amount']
    list_filter=['status_choice']


    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(PaymentRequest, PaymentRequestAdmin)
admin.site.register(PaymentAccount, PaymentAccountAdmin)












