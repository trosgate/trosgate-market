from django.contrib import admin
from .models import Package, TeamMember, Team, Invitation, TeamChat, AssignMember, Tracking



MAX_OBJECTS = 2

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):  
    list_display = ['type','price', 'ordering']
    list_display_links = ['type','price']
    list_editable = ['ordering']
    # readonly_fields = ['type']
    radio_fields = {'type': admin.HORIZONTAL}    

    fieldsets = (
        ('Merchant Package', {'fields': ('type', 'price', 'ordering',)}),
        ('Merchant Upsell', {'fields': (
            'max_member_per_team', 'max_proposals_allowable_per_team',   
            'monthly_offer_contracts_per_team', 'monthly_projects_applicable_per_team', 
        )}),

    )
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set() 

        if not is_superuser: 
            disabled_fields |= {
                'type',
                'price', 
                'status',  
                'ordering',
                'max_member_per_team',
                'monthly_offer_contracts_per_team',
                'max_proposals_allowable_per_team',
                'monthly_projects_applicable_per_team',
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


class TeamMemberAdmin(admin.TabularInline):
    model=TeamMember
    list_display = ['member', 'team', 'earning_ratio', 'status',]
    readonly_fields = ['member', 'team', 'earning_ratio', 'status',]
    list_editable = ['earning_ratio', 'status',]
    extra = 0

    fieldsets = (
        ('Comment Thread', {'fields': ('member', 'earning_ratio', 'status',)}),
    )


class InvitationAdmin(admin.TabularInline):
    model=Invitation
    list_display = ['email','sender','receiver', 'code', 'sent_on', 'status']
    readonly_fields = ['email','sender','receiver', 'code', 'sent_on', 'status']
    extra = 0
    can_delete = False

    fieldsets = (
        ('Invite', {'fields': ('email','sender','receiver', 'code', 'sent_on', 'status')}),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['title', 'merchant', 'package', 'team_balance', 'status',]
    list_display_links = ['title', 'merchant']
    search_fields = ['title']
    list_filter =  ['merchant']
    inlines = [InvitationAdmin, TeamMemberAdmin]
    readonly_fields = [
        'title', 'merchant', 'slug', 'team_balance','created_by','members', 'package_expiry',
        'stripe_customer_id','stripe_subscription_id',
        'paypal_customer_id', 'paypal_subscription_id',
        'razorpay_payment_id','razorpay_payment_url','razorpay_subscription_id',  
    ]

    fieldsets = (
        ('Introduction', {'fields': ('title', 'merchant', 'slug',  'status', 'team_balance',)}),
        ('Package and Background', {'fields': ('package', 'package_status', 'created_by','members','notice',)}),
        ('Subscription Type - Stripe', {'fields': ('stripe_customer_id','stripe_subscription_id',)}),
        ('Subscription Type - Razorpay', {'fields': ('razorpay_payment_id','razorpay_subscription_id','razorpay_payment_url',)}),
        ('Subscription Type - PayPal', {'fields': ('paypal_customer_id','paypal_subscription_id',)}),
    )  

    radio_fields = {
        'status': admin.HORIZONTAL,
        'package_status': admin.HORIZONTAL,
        'package': admin.HORIZONTAL,
    }

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

