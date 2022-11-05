from django.contrib import admin
from .models import Package, Team, Invitation, TeamChat, AssignMember, Tracking

MAX_OBJECTS = 2


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):  
    list_display = ['type','price', 'is_default', 'status', 'verbose_type', 'ordering']
    list_display_links = ['type','status']
    excludes = ['daily_Handshake_mails_to_clients']
    readonly_fields = ['type', 'daily_Handshake_mails_to_clients']
    radio_fields = {'is_default': admin.HORIZONTAL}    

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set() 

        if not is_superuser: 
            disabled_fields |= {
                'type',
                'price', 
                'is_default', 
                'status', 
                'verbose_type', 
                'ordering',
                'max_member_per_team',
                'monthly_offer_contracts_per_team',
                'max_proposals_allowable_per_team',
                'monthly_projects_applicable_per_team',
                'daily_Handshake_mails_to_clients'
            }

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True
        
        return form

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


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'package_status', 'team_balance', 'status',]
    list_display_links = ['title', 'package_status']
    search_fields = ['title']
    list_filter =  ['package']
    readonly_fields = [
        'title', 'slug', 'team_balance','notice','created_by','members', 'package_expiry',
        'stripe_customer_id','stripe_subscription_id',
        'paypal_customer_id', 'paypal_subscription_id',
        'razorpay_payment_id','razorpay_payment_url','razorpay_subscription_id',  
    ]

    fieldsets = (
        ('Introduction', {'fields': ('title', 'slug',  'status', 'team_balance',)}),
        ('Package and Background', {'fields': ('package','package_status', 'created_by','members','notice',)}),
        ('Subscription Type - Stripe', {'fields': ('stripe_customer_id','stripe_subscription_id',)}),
        ('Subscription Type - Razorpay', {'fields': ('razorpay_payment_id','razorpay_subscription_id','razorpay_payment_url',)}),
        ('Subscription Type - PayPal', {'fields': ('paypal_customer_id','paypal_subscription_id',)}),
    )  

    radio_fields = {'status': admin.HORIZONTAL}

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set() 

        if not is_superuser: 
            disabled_fields |= {
                'title',
                'slug',
                'status',
                'package_status',
                'package' 
            }

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True
        
        return form

    def has_add_permission(self, request):
        return False
        
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['email','team', 'code', 'sent_on', 'status']
    list_display_links = ['email', 'team']
    search_fields = ['code','email']
    list_filter = ['status']
    readonly_fields = ['email','team', 'sender','receiver', 'type','code', 'sent_on']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set() 

        if not is_superuser: 
            disabled_fields |= {
                'status'
            }

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True
        
        return form

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

