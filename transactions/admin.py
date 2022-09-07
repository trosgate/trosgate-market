from django.contrib import admin
from . models import OneClickPurchase, Purchase, ApplicationSale, ProposalSale, ContractSale, SubscriptionItem
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from .forms import ProposalRefundForm


class OneClickPurchaseAdmin(admin.ModelAdmin):
    model = OneClickPurchase
    list_display = ['client', 'category', 'salary_paid', 'earning_fee', 'total_earning', 'status']
    list_filter = ['category']
    readonly_fields = [
        'client', 'payment_method','salary_paid','created_at','reference',
        'client', 'payment_method', 'salary_paid', 'earning_fee', 'total_earning', 'status',
        'team', 'category', 'proposal','contract'
    ]
    fieldsets = (
        ('Transaction Details', {'fields': ('client', 'payment_method', 'salary_paid', 'earning_fee', 'total_earning', 'status', 'reference', 'created_at',)}),
        ('Product Type', {'fields': ('team', 'category', 'proposal','contract')}),
        
    )

class PurchaseAdmin(admin.ModelAdmin):
    model = Purchase
    list_display = ['client', 'category', 'payment_method','salary_paid', 'client_fee', 'created_at', 'status']
    list_filter = ['status']
    readonly_fields = ['client', 'payment_method','salary_paid','created_at'] # 'status',
    fieldsets = (
        ('Transaction Details', {'fields': ('client', 'category', 'status','salary_paid', 'unique_reference', 'created_at',)}),
        ('PayPal Payment Mode (If PayPal was used)', {'fields': ('paypal_order_key',)}),
        ('Stripe Payment Mode (If Stripe was used)', {'fields': ('stripe_order_key',)}),
        ('Flutterwave Payment Mode (If Flutterwave was used)', {'fields': ('flutterwave_order_key',)}),
        ('Razorpay Payment Mode (If Razorpay was used)', {'fields': ('razorpay_order_key', 'razorpay_payment_id', 'razorpay_signature',)}),
    )


class ApplicationSaleAdmin(admin.ModelAdmin):
    model = ApplicationSale
    list_display = ['team', 'created_at', 'sales_price', 'disc_sales_price', 'staff_hired', 'total_earning_fee', 'total_discount', 'total_earning','status_value']    
    list_filter = ['team', 'purchase__status']
    readonly_fields = [
         'purchase','project', 'sales_price', 'earning_fee_charged','discount_offered',
        'staff_hired','earning','created_at','updated_at','status_value',
    ]
    fieldsets = (
        ('Classification', {'fields': ('team', 'purchase','project',)}),
        ('Revenue', {'fields': ('sales_price', 'earning_fee_charged','discount_offered',)}),
        ('Earning/Profit', {'fields': ('staff_hired','earning',)}),
        ('Timestamp', {'fields': ('created_at','updated_at','status_value',)}),
    )


class ProposalSaleAdmin(admin.ModelAdmin):
    model = ProposalSale
    list_display = [
        'team', 'created_at','total_sales_price', 'status_value', 'is_refunded', 'admin_action'
    ]    
    list_filter = ['purchase__status']
    readonly_fields = [
        'team', 'purchase','proposal', 'sales_price', 'earning_fee_charged','discount_offered',
        'staff_hired','earning','created_at','updated_at','status_value','is_refunded','total_earning_fee_charged'
    ]
    fieldsets = (
        ('Classification', {'fields': ('team', 'purchase','proposal',)}),
        ('Revenue', {'fields': (
            'sales_price', 'earning_fee_charged','total_earning_fee_charged', 
            'discount_offered','is_refunded',
        )}),
        ('Earning/Profit', {'fields': ('staff_hired','earning',)}),
        ('Timestamp', {'fields': ('created_at','updated_at','status_value',)}),
    )

    def get_urls(self):
        urls = super().get_urls()
        pattern = [
            path('<int:pk>/refund/', self.admin_site.admin_view(self.approve_refund), name='approve-refund'),
        ]
        return pattern + urls


    def admin_action(self, obj):
        return format_html(
            '<a class="button" href="{}"> Issue Refund</a>',
            reverse('admin:approve-refund', args=[obj.pk]),
        )
    
    admin_action.allow_tags = True
    admin_action.short_description = 'Admin Action'

    def approve_refund(self, request, pk, *args, **kwargs):
        return self.process_action(
            request=request,
            pk=pk,
            action_form=ProposalRefundForm,
            action_title='About to issue refund. Action is irreversible so be sure',
        )

    def process_action(self, request, pk, action_form, action_title):
        account = self.get_object(request, pk)
        form = ''
        error_message = ''
        if request.method != 'POST':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                try:
                    form.save(pk)
                except Exception as e:
                    error_message = str(e)
                    print(error_message)
                    pass
                else:
                    self.message_user(request, 'Successfully made refund')
                    url = reverse('admin:transactions_proposalsale_change', args=[pk], current_app=self.admin_site.name)
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['account'] = account
        context['title'] = action_title

        return TemplateResponse(request, 'admin/account/admin_refund.html', context)


    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ContractSaleAdmin(admin.ModelAdmin):
    model = ContractSale
    list_display = [
        'team', 'created_at', 'sales_price', 'disc_sales_price','staff_hired', 'total_sales_price', 
        'earning_fee_charged','total_earning_fee_charged', 'total_discount_offered', 'total_earning','status_value'
    ]    
    list_filter = ['purchase__status']
    readonly_fields = [
        'team', 'purchase','contract', 'sales_price', 'earning_fee_charged','discount_offered',
        'staff_hired','earning','created_at','updated_at','status_value',
    ]
    fieldsets = (
        ('Classification', {'fields': ('team', 'purchase','contract',)}),
        ('Revenue', {'fields': (
            'sales_price', 'earning_fee_charged','total_earning_fee_charged', 
            'discount_offered',
        )}),
        ('Earning/Profit', {'fields': ('staff_hired','earning',)}),
        ('Timestamp', {'fields': ('created_at','updated_at','status_value',)}),
    )


    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class SubscriptionItemAdmin(admin.ModelAdmin):
    model = SubscriptionItem
    list_display = ['team', 'subscription_id', 'payment_method', 'price', 'status', 'activation_time','expired_time']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Customer', {'fields': ('team', 'customer_id', 'subscription_id',)}),
        ('State and Attributes', {'fields': ('price', 'status','payment_method',)}),
        ('Timestamp', {'fields': ('created_at', 'activation_time','expired_time',)}),
    )


    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(OneClickPurchase, OneClickPurchaseAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(ApplicationSale, ApplicationSaleAdmin)
admin.site.register(ProposalSale, ProposalSaleAdmin)
admin.site.register(ContractSale, ContractSaleAdmin)
admin.site.register(SubscriptionItem, SubscriptionItemAdmin)
