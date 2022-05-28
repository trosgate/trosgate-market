from django.contrib import admin
from . models import Purchase, ApplicationSale, ProposalSale, ContractSale, SalesReporting, SubscriptionItem


class PurchaseAdmin(admin.ModelAdmin):
    model = Purchase
    list_display = ['client', 'payment_method','salary_paid', 'created_at', 'status']
    list_filter = ['status']
    readonly_fields = ['client', 'payment_method','salary_paid','created_at'] # 'status',
    fieldsets = (
        ('Transaction Details', {'fields': ('client', 'status','salary_paid', 'unique_reference', 'created_at',)}),
        ('PayPal Payment Mode (If PayPal was used)', {'fields': ('paypal_order_key',)}),
        ('Stripe Payment Mode (If Stripe was used)', {'fields': ('stripe_order_key',)}),
        ('Flutterwave Payment Mode (If Flutterwave was used)', {'fields': ('flutterwave_order_key',)}),
        ('Razorpay Payment Mode (If Razorpay was used)', {'fields': ('razorpay_order_key', 'razorpay_payment_id', 'razorpay_signature',)}),
    )


class ApplicationSaleAdmin(admin.ModelAdmin):
    model = ApplicationSale
    list_display = ['team', 'created_at', 'staff_hired', 'sales_price', 'total_earning_fee', 'total_discount', 'total_earning','status_value']    
    list_filter = ['purchase__status']
    readonly_fields = [
        'team', 'purchase','project', 'sales_price', 'earning_fee_charged','discount_offered',
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
        'team', 'created_at', 'staff_hired', 'total_sales_price', 
        'total_earning_fee_charged', 'Total_discount_offered', 'total_earning','status_value'
    ]    
    list_filter = ['purchase__status']
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
        'team', 'created_at', 'staff_hired', 'total_sales_price', 
        'total_earning_fee_charged', 'Total_discount_offered', 'total_earning','status_value'
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

class SalesReportingAdmin(admin.ModelAdmin):
    model = SalesReporting
    list_display = ['team', 'sales_category','created_at', 'staff_hired', 'total_sales_price', 'client_fee_charged','total_freelancer_fee_charged', 'Total_discount_offered', 'total_earning','status_value']
    list_filter = ['sales_category']
    readonly_fields = [
        'team', 'sales_category','purchase','created_at', 'staff_hired', 'total_sales_price', 
        'client_fee_charged','freelancer_fee_charged', 'Total_discount_offered', 
        'total_earning','status_value','earning','created_at','updated_at','status_value'
    ]
    fieldsets = (
        ('Classification', {'fields': ('team', 'purchase','sales_category',)}),
        ('Revenue', {'fields': ('total_sales_price', 'client_fee_charged', 'total_freelancer_fee_charged', 'Total_discount_offered',)}),
        ('Earning/Profit', {'fields': ('staff_hired','earning',)}),
        ('Timestamp', {'fields': ('created_at','updated_at','status_value',)}),
    )


class SubscriptionItemAdmin(admin.ModelAdmin):
    model = SubscriptionItem
    list_display = ['subscriber', 'team', 'payment_method', 'price', 'created_at', ]


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(ApplicationSale, ApplicationSaleAdmin)
admin.site.register(ProposalSale, ProposalSaleAdmin)
admin.site.register(ContractSale, ContractSaleAdmin)
admin.site.register(SalesReporting, SalesReportingAdmin)
admin.site.register(SubscriptionItem, SubscriptionItemAdmin)
