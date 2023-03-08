import sys
from django.contrib import admin
from . models import (
    Category, Department, Skill, Size, ProposalGuides,
    WebsiteSetting, AutoLogoutSystem, Currency, StorageBuckets
)

MAX_OBJECTS = 1
MAX_GATEWAYS = 4



@admin.register(StorageBuckets)
class StorageBucketsAdmin(admin.ModelAdmin):
    list_display = ['description', 'storage_type',]
    exclude = ['description']
    radio_fields = {'storage_type': admin.HORIZONTAL}
    fieldsets = (
        ('Storage Type', {'fields': ('storage_type',)}),
        ('Extra Amazon S3 Bucket Settings - Please fallback on local storage. Amazon S3 module has known bug that will be fixed in update', {'fields': ('bucket_name','access_key','secret_key',)}),
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'preview', 'visible', 'image_tag', ]
    list_filter = ['name']
    search_fields = ['name']
    readonly_fields = ['image_tag']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(WebsiteSetting)
class WebsiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_domain', 'tagline', 'site_logo_tag', ]
    list_display_links = ['site_name', 'site_domain']
    readonly_fields = ['site_logo_tag']
    list_per_page = sys.maxsize
    fieldsets = (
        ('Site Description', {'fields': ('site_name', 'tagline', 'site_Logo',
         'protocol', 'site_domain', 'site_description',)}), 
        ('Color Scheme', {'fields': ('button_color', 'navbar_color',)}),
        ('Social Media', {'fields': ('twitter_url', 'instagram_url', 'youtube_url', 'facebook_url',)}),
        ('Advertisement', {'fields': ('brand_ambassador_image', 'ad_image',)}),
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


@admin.register(AutoLogoutSystem)
class AutoLogoutSystemAdmin(admin.ModelAdmin):
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


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'symbol', 'ordering', 'supported', 'default']
    list_display_links = ['name', 'code']
    list_editable = ['ordering', 'supported', 'default']
    radio_fields = {'supported': admin.HORIZONTAL}
    actions = ['Activate_Currencies', 'Deactivate_Currencies']
    search_fields = ('name', 'code',)
    list_filter = ['supported','default']
    list_per_page = sys.maxsize

    def get_queryset(self, request):
        qs = super(CurrencyAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.all()  
        else:
            return qs.filter(pk=request.user.country.id) 

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set() 

        if not is_superuser:            
            disabled_fields |= {
                'name', 
                'code', 
                'symbol', 
                'ordering', 
                'supported', 
                'default'               
            }
        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True
        
        return form

    def Activate_Currencies(self, request, queryset):
        queryset.update(supported=True)

    def Deactivate_Currencies(self, request, queryset):
        queryset.update(supported=False)

    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Department)
admin.site.register(Size)
admin.site.register(Skill)
admin.site.register(ProposalGuides)

