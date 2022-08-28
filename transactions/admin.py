from django.contrib import admin
from . models import OneClickPurchase, Purchase, ApplicationSale, ProposalSale, ContractSale, SubscriptionItem


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
        'team', 'created_at', 'sales_price','disc_sales_price', 'staff_hired', 'total_sales_price', 
        'total_earning_fee_charged', 'total_discount_offered', 'earning', 'total_earning','status_value'
    ]    
    list_filter = ['team', 'purchase__status']
    readonly_fields = [
        'team', 'purchase','proposal', 'sales_price', 'earning_fee_charged','discount_offered',
        'staff_hired','earning','created_at','updated_at','status_value',
    ]
    fieldsets = (
        ('Classification', {'fields': ('team', 'purchase','proposal',)}),
        ('Revenue', {'fields': (
            'sales_price', 'earning_fee_charged','total_earning_fee_charged', 
            'discount_offered',
        )}),
        ('Earning/Profit', {'fields': ('staff_hired','earning',)}),
        ('Timestamp', {'fields': ('created_at','updated_at','status_value',)}),
    )


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


class SubscriptionItemAdmin(admin.ModelAdmin):
    model = SubscriptionItem
    list_display = ['team', 'subscription_id', 'payment_method', 'price', 'status', 'activation_time','expired_time']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Customer', {'fields': ('team', 'customer_id', 'subscription_id',)}),
        ('State and Attributes', {'fields': ('price', 'status','payment_method',)}),
        ('Timestamp', {'fields': ('created_at', 'activation_time','expired_time',)}),
    )

admin.site.register(OneClickPurchase, OneClickPurchaseAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(ApplicationSale, ApplicationSaleAdmin)
admin.site.register(ProposalSale, ProposalSaleAdmin)
admin.site.register(ContractSale, ContractSaleAdmin)
admin.site.register(SubscriptionItem, SubscriptionItemAdmin)
