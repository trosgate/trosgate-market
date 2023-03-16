from django.contrib import admin
from .models import Team, Invitation, TeamChat, AssignMember, Tracking


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['title', 'merchant', 'created_at', 'team_balance', 'status',]
    list_display_links = ['title', 'merchant']
    search_fields = ['title']
    list_filter =  ['merchant']
    readonly_fields = [
        'title', 'merchant', 'slug', 'team_balance','notice','created_by','members', 'package_expiry',
        'stripe_customer_id','stripe_subscription_id',
        'paypal_customer_id', 'paypal_subscription_id',
        'razorpay_payment_id','razorpay_payment_url','razorpay_subscription_id',  
    ]

    fieldsets = (
        ('Introduction', {'fields': ('title', 'merchant', 'slug',  'status', 'team_balance',)}),
        ('Package and Background', {'fields': ('package_status', 'created_by','members','notice',)}),
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
    list_display = ['email','merchant', 'team', 'code', 'sent_on', 'status']
    list_display_links = ['email', 'merchant', 'team']
    search_fields = ['code','email']
    list_filter = ['status']
    readonly_fields = ['merchant', 'email','team', 'sender','receiver', 'type','code', 'sent_on']

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

