import sys
from django.contrib import admin
from . models import (
    PaydayController, PaymentsController, DepositController, DepositSetting,
    HiringSetting, DiscountSettings,
    MailerSetting, TestMailSetting, SubscriptionSetting, ExchangeRateSetting,
    GatewaySetting
)

MAX_OBJECTS = 1
MAX_GATEWAYS = 7



@admin.register(PaydayController)
class PaydayAdmin(admin.ModelAdmin):
    list_display = ['preview','payday_converter']
    list_editable = ['payday_converter']
    readonly_fields = ['preview']
    fieldsets = (
        ('Preview', {'fields': ('preview',)}),
        ('Payday Duration', {'fields': ('payday_converter',)}),
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


@admin.register(PaymentsController)
class PaymentControlAdmin(admin.ModelAdmin):
    list_display = ['preview', 'min_balance', 'max_receiver_balance', 'min_transfer', 'max_transfer', 'min_withdrawal', 'max_withdrawal']
    list_display_links = ['preview']
    list_editable = ['min_balance', 'max_receiver_balance', 'min_transfer', 'max_transfer', 'min_withdrawal', 'max_withdrawal']
    readonly_fields = ['preview']
    list_per_page = sys.maxsize

    fieldsets = (
        ('Balance Control', {'fields': ('min_balance', 'max_receiver_balance',)}),
        ('Transfer Control', {'fields': ('min_transfer', 'max_transfer',)}),
        ('Withdrawal Control', {'fields': ('min_withdrawal', 'max_withdrawal',)}),
        
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DepositController)
class DepositControlAdmin(admin.ModelAdmin):
    list_display = ['preview', 'min_balance', 'max_balance', 'min_deposit', 'max_deposit']
    list_display_links = ['preview']
    list_editable = ['min_balance', 'max_balance', 'min_deposit', 'max_deposit']
    list_per_page = sys.maxsize

    fieldsets = (
        ('Balance Control', {'fields': ('min_balance', 'max_balance',)}),
        ('Deposit Control', {'fields': ('min_deposit', 'max_deposit',)}),
        
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ExchangeRateSetting)
class ExachangeRateAPIAdmin(admin.ModelAdmin):
    list_display = ['preview', 'exchange_rates_api_key']
    list_display_links = ['preview']
    list_editable = ['exchange_rates_api_key']

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


@admin.register(GatewaySetting)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ['name', 'processing_fee', 'subscription', 'status', 'ordering']
    list_editable = ['status', 'ordering']
    list_display_links = ['name', 'processing_fee']
    readonly_fields = ['default']
    fieldsets = (
        ('Gateway Activation Settings', {'fields': (
            'name', 'processing_fee','default', 'ordering','status',
        )}),
        ('Subscription Payment APIs', {'fields': ('public_key',
            'secret_key', 'webhook_key','subscription_price_id', 'sandbox','subscription',)}),
    )
    radio_fields = {
        'subscription': admin.HORIZONTAL,
        'status': admin.HORIZONTAL,
        }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set() 

        
        if obj is not None and obj.name == 'balance':
            disabled_fields |= {                
                'public_key',
                'secret_key',
                'webhook_key',
                'subscription_price_id',
                'sandbox',
                'subscription',
            }

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True
        
        return form

    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_GATEWAYS:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


# @admin.register(PaymentAPISetting)
# class PaymentAPIsAdmin(admin.ModelAdmin):
#     list_display = ['preview']
#     list_display_links = ['preview']
#     readonly_fields = ['preview']
#     radio_fields = {'sandbox': admin.HORIZONTAL}
#     fieldsets = (
#         ('API Environment', {'fields': ('sandbox',)}),
#         ('Stripe Payment API', {'fields': ('stripe_public_key',
#          'stripe_secret_key', 'stripe_webhook_key','stripe_subscription_price_id', 'stripe_active',)}),
#         ('PayPal Payment API', {
#          'fields': ('paypal_public_key', 'paypal_secret_key', 'paypal_subscription_price_id', 'paypal_active',)}),
#         ('Flutterwave Payment API', {
#          'fields': ('flutterwave_public_key', 'flutterwave_secret_key','flutterwave_secret_hash', 'flutterwave_active',)}),
#         ('Razorpay Payment API', {
#          'fields': ('razorpay_public_key_id', 'razorpay_secret_key_id', 'razorpay_subscription_price_id','razorpay_active',)}),
#         ('MTN Momo API', {
#          'fields': ('mtn_api_user_id', 'mtn_api_key', 'mtn_subscription_key','mtn_callback_url','mtn_active',)}),
#     )

#     def has_add_permission(self, request):
#         if self.model.objects.count() >= MAX_OBJECTS:
#             return False
#         return super().has_add_permission(request)

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_actions(self, request):
#         actions = super().get_actions(request)

#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions


@admin.register(HiringSetting)
class HiringFeeAdmin(admin.ModelAdmin):
    list_display = ['preview', 'contract_percentage',
                    'proposal_percentage', 'application_percentage']
    list_display_links = ['preview']
    readonly_fields = ['contract_percentage',
                       'proposal_percentage', 'application_percentage']
    fieldsets = (
        ('External Contract Fee - It is single fee because freelancer did the hard job of getting client', {'fields': ('extcontract_fee_percentage',)}),
        ('Internal Contract Fee Structure', {'fields': (
            'contract_fee_percentage', 'contract_fee_extra', 'contract_delta_amount',)}),
        ('Proposal Fee Structure', {'fields': (
            'proposal_fee_percentage', 'proposal_fee_extra', 'proposal_delta_amount',)}),
        ('Application Fee Structure', {'fields': (
            'application_fee_percentage', 'application_fee_extra', 'application_delta_amount',)}),

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


@admin.register(DiscountSettings)
class DiscountSystemAdmin(admin.ModelAdmin):
    list_display = ['preview', 'level_one_discount', 'level_two_discount', 'level_three_discount', 'level_four_discount']
    list_display_links = ['preview']
    readonly_fields = ['level_one_name', 'level_two_name', 'level_three_name', 'level_four_name']
    fieldsets = (
        ('Level One Checkout Discount', {'fields': (
            'level_one_name', 'level_one_rate', 'level_one_start_amount', 'level_one_delta_amount',)}),
        ('Level Two Checkout Discount', {'fields': (
            'level_two_name', 'level_two_rate', 'level_two_start_amount', 'level_two_delta_amount',)}),
        ('Level Three Checkout Discount', {'fields': (
            'level_three_name', 'level_three_rate', 'level_three_start_amount', 'level_three_delta_amount',)}),
        ('Level Four Checkout Discount', {
         'fields': ('level_four_name', 'level_four_rate', 'level_four_start_amount',)}),
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


@admin.register(MailerSetting)
class MailerAdmin(admin.ModelAdmin):
    list_display = ['from_email', 'email_hosting_server', 'email_use_tls', 'email_use_ssl']
    list_display_links = ['from_email', 'email_hosting_server']
    list_per_page = sys.maxsize
    fieldsets = (
        ('SMTP Email API', {'fields': ('email_hosting_server','email_hosting_username', 'from_email', 'email_hosting_server_password',
         'email_hosting_server_port',)}),
        ('Email Server Certificate', {'fields': ('email_use_tls', 'email_use_ssl',)}),
        ('Email Config Error Control', {'fields': ('email_timeout', 'email_fail_silently',)}),
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


@admin.register(TestMailSetting)
class TestEmailAdmin(admin.ModelAdmin):
    list_display = ['title', 'test_email']
    list_display_links = ['title', 'test_email']
    readonly_fields = ['title']
    fieldsets = (
        ('Description', {'fields': ('title',)}),
        ('Receiver Email: Enter email and click "Save" button to send Test mail', {'fields': ('test_email',)}),
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


@admin.register(SubscriptionSetting)
class SubscriptionGatewayAdmin(admin.ModelAdmin):
    list_display = ['name', 'paypal', 'stripe', 'razorpay', 'flutterwave']
    list_editable = ['paypal', 'stripe', 'razorpay', 'flutterwave']
    list_display_links = ['name']
    # readonly_fields = ['name']
    fieldsets = (
        ('Paypal Config', {'fields': ('paypal',)}),
        ('Stripe Config', {'fields': ('stripe',)}),
        ('Razorpay Config', {'fields': ('razorpay',)}),
        ('Flutterwave Config', {'fields': ('flutterwave',)}),
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


@admin.register(DepositSetting)
class DepositSettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'paypal', 'stripe', 'razorpay', 'flutterwave']
    list_editable = ['paypal', 'stripe', 'razorpay', 'flutterwave']
    list_display_links = ['name']
    # readonly_fields = ['name']
    fieldsets = (
        ('Paypal Config', {'fields': ('paypal',)}),
        ('Stripe Config', {'fields': ('stripe',)}),
        ('Razorpay Config', {'fields': ('razorpay',)}),
        ('Flutterwave Config', {'fields': ('flutterwave',)}),
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




















































































