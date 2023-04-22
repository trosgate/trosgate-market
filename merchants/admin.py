from django.contrib import admin
# from .models import Merchant


# @admin.register(Merchant)
# class MerchantAdmin(admin.ModelAdmin):   
#     list_display = ['business_name', 'merchant', 'type', 'package', 'created_at']
#     radio_fields = {'type': admin.HORIZONTAL}    
#     readonly_fields = [
#         'business_name', 'merchant', 'package', 'members', 'created_at', 'modified', 'tagline', 'description',
#         'profile_photo', 'image_tag', 'banner_photo',  'banner_tag','address','announcement', 
#         'company_logo', 'logo_tag', 'get_merchant','gender', 'get_site','gateways', 
#     ]
#     # list_display_links = None  
#     fieldsets = (
#         ('Personal Information', {'fields': (
#             'business_name', 'get_merchant', 'gender', 'address',
#         )}),
#         ('Personal & Business Media', {'fields': (
#             'profile_photo', 'image_tag', 'banner_photo',  'banner_tag', 
#             'company_logo', 'logo_tag',
#         )}),
#         ('Website and Content', {'fields': ('get_site', 'tagline', 'description','announcement',)}),
#         ('Gateways and Staffs', {'fields': ('gateways', 'members',)}),
#         ('Activity Log', {'fields': ('created_at', 'modified',)}),
#     )

#     @admin.display(description='Merchant Types', ordering='merchant__user_type')
#     def get_user_type(self, obj):
#         return obj.merchant.user_type.capitalize()

#     @admin.display(description='Merchant', ordering='merchant__first_name')
#     def get_merchant(self, obj):
#         return obj.merchant.get_full_name()
    
#     @admin.display(description='Website', ordering='site')
#     def get_site(self, obj):
#         return f"Domain: {obj.site.domain} - Name: {obj.site.name}"

#     # def has_add_permission(self, request):
#     #     return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_actions(self, request):
#         actions = super().get_actions(request)

#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions

