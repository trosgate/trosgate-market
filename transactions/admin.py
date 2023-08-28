from django.contrib import admin
from . models import Purchase, ApplicationSale, ProposalSale, ContractSale, ExtContract, SubscriptionItem
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from .forms import (
    ProposalRefundForm, 
    ApplicationRefundForm, 
    ContractRefundForm, 
    ExtContractRefundForm,
    OneClickRefundForm
)


# @admin.register(OneClickPurchase)
# class OneClickPurchaseAdmin(admin.ModelAdmin):
#     model = OneClickPurchase
#     list_display = ['client', 'category', 'salary_paid', 'earning_fee', 'total_earning', 'status', 'is_refunded', 'admin_action']
#     list_filter = ['category', 'status']
#     readonly_fields = [
#         'client', 'payment_method','salary_paid','created_at','unique_reference',
#         'client', 'payment_method', 'salary_paid', 'earning_fee', 'total_earning', 'status',
#         'team', 'category', 'proposal','contract','extcontract'
#     ]
#     fieldsets = (
#         ('Transaction Details', {'fields': ('client', 'payment_method', 'salary_paid', 'earning_fee', 'total_earning', 'status', 'unique_reference', 'created_at',)}),
#         ('Product Type', {'fields': ('team', 'category', 'proposal', 'contract', 'extcontract')}),        
#     )


#     def get_urls(self):
#         urls = super().get_urls()
#         pattern = [
#             path('<int:pk>/refund/', self.admin_site.admin_view(self.approve_refund), name='oneclick-refund'),
#         ]
#         return pattern + urls


#     def admin_action(self, obj):
#         return format_html(
#             '<a class="button" href="{}"> Refund</a>',
#             reverse('admin:oneclick-refund', args=[obj.pk]),
#         )
    
#     admin_action.allow_tags = True
#     admin_action.short_description = 'Admin Action'

#     def approve_refund(self, request, pk, *args, **kwargs):
#         return self.process_action(
#             request=request,
#             pk=pk,
#             action_form=OneClickRefundForm,
#             action_title='About to issue refund. Action is irreversible so be sure',
#         )

#     def process_action(self, request, pk, action_form, action_title):
#         account = self.get_object(request, pk)
#         form = ''
#         error_message = ''
#         if request.method != 'POST':
#             form = action_form()
#         else:
#             form = action_form(request.POST)
#             if form.is_valid():
#                 try:
#                     form.save(pk)
#                 except Exception as e:
#                     error_message = str(e)
#                     print(error_message)
#                     pass
#                 else:
#                     self.message_user(request, 'Successfully made refund')
#                     url = reverse('admin:transactions_oneclickpurchase_change', args=[pk], current_app=self.admin_site.name)
#                     return HttpResponseRedirect(url)

#         context = self.admin_site.each_context(request)
#         context['opts'] = self.model._meta
#         context['form'] = form
#         context['account'] = account
#         context['title'] = action_title

#         return TemplateResponse(request, 'admin/account/project_refund.html', context)

#     def has_add_permission(self, request):        
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_actions(self, request):
#         actions = super().get_actions(request)

#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    model = Purchase
    list_display = ['client', 'payment_method','salary_paid', 'client_fee', 'created_at', 'status']
    list_filter = ['category', 'status']
    readonly_fields = [
        'client', 'category', 'status','salary_paid', 'created_at',
        'paypal_order_key', 'paypal_transaction_id', 'stripe_order_key', 
        'paystack_transaction_id','flutterwave_transaction_id','reference',
        'razorpay_order_key', 'razorpay_payment_id', 'razorpay_signature'
        ]  
    fieldsets = (
        ('Transaction Details', {'fields': ('client', 'category', 'status','reference', 'salary_paid','created_at',)}),
        ('PayPal Payment Mode (If PayPal was used)', {'fields': ('paypal_transaction_id',)}),
        ('Stripe Payment Mode (If Stripe was used)', {'fields': ('stripe_order_key',)}),
        ('Paystack Payment Mode (If Paystack was used)', {'fields': ('paystack_transaction_id',)}),
        ('Flutterwave Payment Mode (If Flutterwave was used)', {'fields': ('flutterwave_transaction_id',)}),
        ('Razorpay Payment Mode (If Razorpay was used)', {'fields': ('razorpay_order_key', 'razorpay_payment_id', 'razorpay_signature',)}),
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
    
    # def get_queryset(self, request):
    #     qs = super(PurchaseAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs.all()  
    #     else:
    #         return qs.none() 
    
    
@admin.register(ApplicationSale)
class ApplicationSaleAdmin(admin.ModelAdmin):
    model = ApplicationSale
    list_display = [
        'team', 'created_at','totalsales', 'status_value', 'is_refunded', 'admin_action'
    ]    
    list_filter = ['purchase__status','is_refunded']
    search_fields = ['team__title', 'total_sales_price']    
    readonly_fields = [
        'team', 'purchase','project', 'sales_price', 'total_sales_price', 
        'total_earning', 'earning_fee_charged','discount_offered',
        'staff_hired','earning','created_at','updated_at','status_value',
        'is_refunded','total_earning_fee_charged', 'start_time', 'end_time', 'status',
        'revision','duration',
    ]
    fieldsets = (
        ('Classification', {'fields': ('team', 'purchase','project',)}),
        ('Revenue', {'fields': (
            'total_sales_price', 'earning_fee_charged','total_earning_fee_charged', 
            'discount_offered','is_refunded',
        )}),
        ('Earning/Profit', {'fields': ('staff_hired','earning','total_earning',)}),
        ('Product Attributes', {'fields': ('revision','duration',)}),
        ('Transaction Manager', {'fields': ( 'start_time', 'end_time', 'status')}),
        ('Timestamp', {'fields': ('created_at','updated_at','status_value',)}),
    )

    def get_urls(self):
        urls = super().get_urls()
        pattern = [
            path('<int:pk>/refund/', self.admin_site.admin_view(self.approve_refund), name='application-refund'),
        ]
        return pattern + urls


    def admin_action(self, obj):
        return format_html(
            '<a class="button" href="{}"> Refund</a>',
            reverse('admin:application-refund', args=[obj.pk]),
        )
    
    admin_action.allow_tags = True
    admin_action.short_description = 'Admin Action'

    def approve_refund(self, request, pk, *args, **kwargs):
        return self.process_action(
            request=request,
            pk=pk,
            action_form=ApplicationRefundForm,
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
                    url = reverse('admin:transactions_applicationsale_change', args=[pk], current_app=self.admin_site.name)
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['account'] = account
        context['title'] = action_title

        return TemplateResponse(request, 'admin/account/project_refund.html', context)


    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ProposalSale)
class ProposalSaleAdmin(admin.ModelAdmin):
    model = ProposalSale
    list_display = [
        'team', 'created_at','totalsales', 'status_value', 'is_refunded', 'admin_action'
    ]    
    list_filter = ['purchase__status','is_refunded']
    search_fields = ['team__title', 'reference', 'total_sales_price']    
    readonly_fields = [
        'team', 'purchase','proposal', 'sales_price', 'total_sales_price', 'total_earning', 'earning_fee_charged','discount_offered',
        'staff_hired','earning','created_at','updated_at','status_value','is_refunded','total_earning_fee_charged', 'start_time', 'end_time', 'status',
        'package_name','revision','duration','reference'
    ]
    fieldsets = (
        ('Classification', {'fields': ('team', 'purchase','proposal', 'reference')}),
        ('Revenue', {'fields': (
            'total_sales_price', 'earning_fee_charged','total_earning_fee_charged', 
            'discount_offered','is_refunded',
        )}),
        ('Earning/Profit', {'fields': ('staff_hired','earning','total_earning',)}),
        ('Product Attributes', {'fields': ('package_name','revision','duration',)}),
        ('Transaction Manager', {'fields': ( 'start_time', 'end_time', 'status')}),
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
            '<a class="button" href="{}"> Refund</a>',
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

        return TemplateResponse(request, 'admin/account/proposal_refund.html', context)

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ContractSale)
class ContractSaleAdmin(admin.ModelAdmin):
    model = ContractSale
    list_display = [
        'team', 'created_at','total_sales_price', 'status_value', 'is_refunded', 'admin_action'
    ]    
    list_filter = ['purchase__status','is_refunded']
    search_fields = ['team__title', 'total_sales_price']    
    readonly_fields = [
        'team', 'purchase','contract', 'sales_price', 'total_sales_price', 'total_earning', 'earning_fee_charged','discount_offered',
        'staff_hired','earning','created_at','updated_at','status_value','is_refunded','total_earning_fee_charged'
    ]
    fieldsets = (
        ('Classification', {'fields': ('team', 'purchase','contract',)}),
        ('Revenue', {'fields': (
            'total_sales_price', 'earning_fee_charged','total_earning_fee_charged', 
            'discount_offered','is_refunded',
        )}),
        ('Earning/Profit', {'fields': ('staff_hired','earning','total_earning')}),
        ('Timestamp', {'fields': ('created_at','updated_at','status_value',)}),
    )

    def get_urls(self):
        urls = super().get_urls()
        pattern = [
            path('<int:pk>/refund/', self.admin_site.admin_view(self.approve_refund), name='contract-refund'),
        ]
        return pattern + urls


    def admin_action(self, obj):
        return format_html(
            '<a class="button" href="{}"> Refund</a>',
            reverse('admin:contract-refund', args=[obj.pk]),
        )
    
    admin_action.allow_tags = True
    admin_action.short_description = 'Admin Action'

    def approve_refund(self, request, pk, *args, **kwargs):
        return self.process_action(
            request=request,
            pk=pk,
            action_form=ContractRefundForm,
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
                    url = reverse('admin:transactions_contractsale_change', args=[pk], current_app=self.admin_site.name)
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['account'] = account
        context['title'] = action_title

        return TemplateResponse(request, 'admin/account/contract_refund.html', context)

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ExtContract)
class ExtContractAdmin(admin.ModelAdmin):
    model = ExtContract
    list_display = [
        'team', 'created_at','total_sales_price', 'status_value', 'is_refunded', 'admin_action'
    ]   
    list_filter = ['purchase__status','is_refunded']
    search_fields = ['team__title', 'total_sales_price']    
    readonly_fields = [
        'team', 'purchase','contract', 'sales_price', 'total_sales_price', 'total_earning', 'earning_fee_charged',
        'staff_hired','earning','created_at','updated_at','status_value','is_refunded','total_earning_fee_charged'
    ]
    fieldsets = (
        ('Classification', {'fields': ('team', 'purchase','contract',)}),
        ('Revenue', {'fields': (
            'total_sales_price', 'earning_fee_charged','total_earning_fee_charged','is_refunded',
        )}),
        ('Earning/Profit', {'fields': ('staff_hired','earning','total_earning')}),
        ('Timestamp', {'fields': ('created_at','updated_at','status_value',)}),
    )

    def get_urls(self):
        urls = super().get_urls()
        pattern = [
            path('<int:pk>/refund/', self.admin_site.admin_view(self.approve_refund), name='ext-contract-refund'),
        ]
        return pattern + urls


    def admin_action(self, obj):
        return format_html(
            '<a class="button" href="{}"> Refund</a>',
            reverse('admin:ext-contract-refund', args=[obj.pk]),
        )
    
    admin_action.allow_tags = True
    admin_action.short_description = 'Admin Action'

    def approve_refund(self, request, pk, *args, **kwargs):
        return self.process_action(
            request=request,
            pk=pk,
            action_form=ExtContractRefundForm,
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
                    url = reverse('admin:transactions_extcontract_change', args=[pk], current_app=self.admin_site.name)
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['account'] = account
        context['title'] = action_title

        return TemplateResponse(request, 'admin/account/ext_contract_refund.html', context)

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(SubscriptionItem)
class SubscriptionItemAdmin(admin.ModelAdmin):
    model = SubscriptionItem
    list_display = ['team', 'subscription_id', 'payment_method', 'expired_time']
    search_fields = ['team__title', 'subscription_id', 'customer_id']
    list_filter=['status']
    readonly_fields = [
        'team', 'customer_id', 'subscription_id','created_at',
        'price', 'status','payment_method', 'activation_time','expired_time'
        ]
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

