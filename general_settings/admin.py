import sys
from django.contrib import admin
from . models import (
    Category, Department, Skill, Size, CommunicationLanguage, ProposalGuides,
    WebsiteSetting, PaymentGateway, PaymentAPIs, AutoLogoutSystem, DiscountSystem,
    EmailConfig, TestEmail, SubscriptionGateway, HiringFee, Currency, ExachangeRateAPI,
    PaymentsControl, Mailer, DepositControl
)

MAX_OBJECTS = 1
MAX_GATEWAYS = 4


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name', 'preview', 'visible', 'image_tag', ]
    list_filter = ['name']
    search_fields = ['name']
    readonly_fields = ['image_tag']
    prepopulated_fields = {'slug': ('name',)}


class WebsiteSettingAdmin(admin.ModelAdmin):
    model = WebsiteSetting
    list_display = ['site_name', 'site_domain', 'tagline', 'site_logo_tag', ]
    list_display_links = ['site_name', 'site_domain']
    readonly_fields = ['site_logo_tag']
    list_per_page = sys.maxsize
    fieldsets = (
        ('Site Description', {'fields': ('site_name', 'tagline', 'site_Logo',
         'protocol', 'www', 'site_domain', 'site_url', 'site_description',)}),
    )

    radio_fields = {'protocol': admin.HORIZONTAL}

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


class MailerAdmin(admin.ModelAdmin):
    model = Mailer
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



class TestEmailAdmin(admin.ModelAdmin):
    model = TestEmail
    list_display = ['title', 'test_email']
    list_display_links = ['title', 'test_email']
    readonly_fields = ['title']
    fieldsets = (
        ('Description', {'fields': ('title',)}),
        ('Receiver Email', {'fields': ('test_email',)}),
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


class PaymentGatewayAdmin(admin.ModelAdmin):
    model = PaymentGateway
    list_display = ['name', 'default', 'processing_fee', 'status', 'ordering']
    list_editable = ['processing_fee', 'default', 'status', 'ordering']
    # readonly_fields = ['name']

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


class SubscriptionGatewayAdmin(admin.ModelAdmin):
    model = SubscriptionGateway
    list_display = ['name', 'default', 'processing_fee', 'status', 'ordering']
    list_editable = ['processing_fee', 'default', 'status', 'ordering']
    readonly_fields = ['name']

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


class PaymentAPIsAdmin(admin.ModelAdmin):
    model = PaymentAPIs
    list_display = ['preview', 'gateway_count']
    list_display_links = ['preview', 'gateway_count']
    readonly_fields = ['preview']
    radio_fields = {'sandbox': admin.HORIZONTAL}
    fieldsets = (
        ('API Environment', {'fields': ('sandbox',)}),
        ('Stripe API', {'fields': ('stripe_public_key',
         'stripe_secret_key', 'stripe_webhook_key',)}),
        ('Stripe Package Subscription', {
         'fields': ('stripe_subscription_price_id',)}),
        ('PayPal API', {
         'fields': ('paypal_public_key', 'paypal_secret_key', 'paypal_subscription_price_id',)}),
        ('Flutterwave API', {
         'fields': ('flutterwave_public_key', 'flutterwave_secret_key','flutterwave_secret_hash',)}),
        ('Razorpay API', {
         'fields': ('razorpay_public_key_id', 'razorpay_secret_key_id', 'razorpay_subscription_price_id',)}),
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


class AutoLogoutSystemAdmin(admin.ModelAdmin):
    model = AutoLogoutSystem
    list_display = ['preview', 'warning_time_schedule', 'interval']
    list_display_links = ['preview']
    list_editable = ['warning_time_schedule', 'interval']

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


class DiscountSystemAdmin(admin.ModelAdmin):
    model = DiscountSystem
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


class HiringFeeAdmin(admin.ModelAdmin):
    model = HiringFee
    list_display = ['preview', 'contract_percentage',
                    'proposal_percentage', 'application_percentage']
    list_display_links = ['preview']
    readonly_fields = ['contract_percentage',
                       'proposal_percentage', 'application_percentage']
    fieldsets = (
        ('Contract Fee Structure', {'fields': (
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


class CurrencyAdmin(admin.ModelAdmin):
    model = Currency
    list_display = ['name', 'code', 'symbol', 'ordering', 'supported', 'default']
    list_display_links = ['name', 'code']
    list_editable = ['ordering', 'supported', 'default']
    radio_fields = {'supported': admin.HORIZONTAL}
    actions = ['Activate_Currencies', 'Deactivate_Currencies']
    search_fields = ('name', 'code',)
    list_filter = ('supported',)
    list_per_page = sys.maxsize

    def Activate_Currencies(self, request, queryset):
        queryset.update(supported=True)

    def Deactivate_Currencies(self, request, queryset):
        queryset.update(supported=False)

    def has_add_permission(self, request):
        if self.model.objects.count():
            return False
        return super().has_add_permission(request)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class ExachangeRateAPIAdmin(admin.ModelAdmin):
    model = ExachangeRateAPI
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


class PaymentControlAdmin(admin.ModelAdmin):
    model = PaymentsControl
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


class DepositControlAdmin(admin.ModelAdmin):
    model = DepositControl
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


admin.site.register(WebsiteSetting, WebsiteSettingAdmin)
admin.site.register(PaymentAPIs, PaymentAPIsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PaymentsControl, PaymentControlAdmin)
admin.site.register(Department)
admin.site.register(Size)
admin.site.register(Skill)
admin.site.register(TestEmail, TestEmailAdmin)
admin.site.register(Mailer, MailerAdmin)
admin.site.register(DiscountSystem, DiscountSystemAdmin)
admin.site.register(AutoLogoutSystem, AutoLogoutSystemAdmin)
admin.site.register(PaymentGateway, PaymentGatewayAdmin)
admin.site.register(SubscriptionGateway, SubscriptionGatewayAdmin)
admin.site.register(CommunicationLanguage)
admin.site.register(ProposalGuides)
admin.site.register(HiringFee, HiringFeeAdmin)
admin.site.register(DepositControl, DepositControlAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExachangeRateAPI, ExachangeRateAPIAdmin)
