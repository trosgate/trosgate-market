from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Customer, Country, Package, Merchant, TwoFactorAuth
from django.utils.translation import gettext_lazy as _
import sys
from django.contrib.admin.models import LogEntry
import warnings
from account.management.commands import refresh
from django.core.management import call_command


MAX_PACKAGE = 3


class CustomerCreationForm(forms.ModelForm):
    short_name = forms.CharField(label='Username', min_length=4, max_length=30)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label='Select Country')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = Customer
        fields = ('email', 'user_type', 'short_name','first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomerChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
  
    class Meta:
        model = Customer
        fields = ['email', 'short_name', 'country', 'password', 'is_active', 'is_superuser']

    def clean_password(self):
        return self.initial['password']


@admin.register(Customer)
class CustomerAdmin(BaseUserAdmin,):  
    form = CustomerChangeForm
    add_form = CustomerCreationForm
    actions = ['refresh']

    list_display = ['id', 'get_short_name', 'email', 'is_superuser','user_type', 'is_active', 'last_login']
    readonly_fields = ['site', 'active_merchant_id', 'date_joined', 'user_type', 'last_login']
    list_display_links = ['get_short_name']
    list_filter = ['user_type', 'is_superuser', 'is_assistant','site']
    fieldsets = (
        ('Personal Information', {'fields': ('email', 'short_name', 'first_name', 'last_name', 'phone', 'country', 'password',)}),
        ('All User Permissions', {'fields': ('user_type','is_active','is_staff',)}),
        ('Company Roles', {'fields': ('is_assistant', 'is_superuser',)}),
        ('Activity Log', {'fields': ('site', 'active_merchant_id', 'date_joined', 'last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'short_name', 'country', 'password1', 'password2',)
        }),
    )
    search_fields = ('pk', 'email', 'first_name', 'last_name',)
    ordering = ('email',)
    filter_horizontal = ()
    list_per_page = 50
    is_superuser = False

    def get_queryset(self, request):
        qs = super(CustomerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.all()  
        else:
            return qs.filter(pk=request.user.id, is_staff=True)  


    def has_delete_permission(self, request, obj=None):
        return False


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return super().has_add_permission(request)


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set() 

        if Customer.objects.filter(is_superuser=True).count() > 0:
            disabled_fields |= {
                'is_superuser',
            }

        if not is_superuser:            
            disabled_fields |= {
                'short_name',
                'email',
                'country',                 
                'is_active',
                'is_staff',
                'is_superuser',
                'is_assistant',
            }

        if (not is_superuser and obj is not None and obj == request.user):
            disabled_fields |= {
                'short_name',
                'email',
                'is_active',
                'is_superuser',
                'is_staff',
                'is_assistant',
            }        

        if (not is_superuser and obj is not None and obj != request.user):
            disabled_fields |= {
                'short_name',
                'first_name',
                'last_name',
                'email',
                'phone',
                'country', 
                'password',
                'is_active',
                'is_superuser',
                'is_staff',
                'is_assistant',               
            }

        if obj is not None and obj.user_type == 'freelancer':
            disabled_fields |= {                
                'is_superuser',
                'is_staff',
                'is_assistant',
            }

        if obj is not None and obj.user_type == 'client':
            disabled_fields |= {                
                'is_superuser',
                'is_staff',
                'is_assistant',
            }

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True
        
        return form


    def refresh(self, request, queryset):
        call_command('refresh')
        self.message_user(request, 'Refresh command was sent successfully')
    refresh.short_description = 'Run refresh Command'


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'action_time',  'action_flag']
    readonly_fields = [
        'action_time', 'user', 'content_type', 'action_flag', 
        'object_repr', 'change_message', 'object_id'
    ]
    list_display_links = ['content_type', 'user']
    search_fields = ['object_repr', 'change_message']
    list_filter = ('action_flag',)

    def get_queryset(self, request):
        qs = super(LogEntryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.all()  
        else:
            return qs.filter(user=request.user)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['flag_tag', 'name', 'country_code', 'ordering', 'supported']
    readonly_fields = ['flag_tag']
    list_display_links = ['flag_tag', 'name']
    list_editable = ['ordering', 'supported']
    radio_fields = {'supported': admin.HORIZONTAL}
    actions = ['Activate_Countries', 'Deactivate_Countries']
    search_fields = ('name', 'country_code')
    list_filter = ('supported',)
    list_per_page = sys.maxsize

    def Activate_Countries(self, request, queryset):
        queryset.update(supported=True)

    def Deactivate_Countries(self, request, queryset):
        queryset.update(supported=False)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):  
    list_display = ['type','price', 'is_default', 'verbose_type', 'ordering']
    list_display_links = ['type','verbose_type']
    # excludes = ['daily_Handshake_mails_to_clients']
    readonly_fields = ['ssl_activation']
    radio_fields = {
        'is_default': admin.HORIZONTAL, 
        'can_change_domain':admin.HORIZONTAL,
        'can_upsell_teams':admin.HORIZONTAL,
        'ssl_activation':admin.HORIZONTAL,
        'multiple_freelancer_teams':admin.HORIZONTAL,
    }    
    fieldsets = (
        ('Merchant Package', {'fields': (
            'type', 'price', 'verbose_type', 'can_change_domain', 'ssl_activation','max_num_of_staff',
            'can_upsell_teams', 'max_users_sitewide','multiple_freelancer_teams', 'ordering',
        )}),
        ('Merchant Upsell', {'fields': (
            'max_member_per_team', 'upsell_price', 'max_proposals_allowable_per_team',  
            'monthly_offer_contracts_per_team', 'monthly_projects_applicable_per_team', 
        )}),

    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        is_admin = request.user.user_type == 'admin'
        disabled_fields = set() 

        if not is_admin: 
            disabled_fields |= {
                'type',
                'price', 
                'is_default', 
                'status', 
                'verbose_type', 
                'ordering',
                'max_num_of_staff',
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
        if self.model.objects.count() >= MAX_PACKAGE:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(TwoFactorAuth)
class TwoFactorAuthAdmin(admin.ModelAdmin):   
    list_display = ['user', 'get_user_type', 'last_login', 'pass_code']
    readonly_fields = ['user', 'last_login', 'pass_code']     
    list_display_links = None

    def get_queryset(self, request):
        qs = super(TwoFactorAuthAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs.all().exclude(user__is_staff=True)  
        else:
            return qs.filter(pk=0)  
            
    @admin.display(description='User Types', ordering='user__user_type')
    def get_user_type(self, obj):
        return obj.user.user_type.capitalize()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):   
    list_display = ['site_logo_tag', 'business_name', 'merchant', 'type', 'package', 'created_at']
    radio_fields = {
        'type': admin.HORIZONTAL,
        'category_type': admin.HORIZONTAL,
        'banner_type': admin.HORIZONTAL,
        'promo_type': admin.HORIZONTAL,
    }    
    readonly_fields = [
        'get_merchant', 'get_site', 'site_logo_tag', 'image_tag', 'banner_tag',
        'merchant', 'package', 'members', 'created_at', 'modified', 'promo_image_tag',
        # 'business_name', 'gender', 'tagline', 'description', 'address', 'announcement',
        # 'gateways','banner_image',,'profile_photo'  
    ]
    # list_display_links = None  
    fieldsets = (
        ('Personal Information', {'fields': (
            'get_merchant', 'gender', 'profile_photo','image_tag', 
        )}),
        ('Business Background', {'fields': (
            'business_name', 'type', 'address','created_at', 'modified',
            'site_Logo','site_logo_tag', 'banner_image','banner_tag', 
        )}),
        ('Website, Banner & Color Scheme', {'fields': (
            'category_type', 'banner_type', 'title_block','subtitle_block','button_color', 'navbar_color',
            'get_site', 'tagline', 'description','announcement','footer_description', 
        )}),
        ('Additional Hero Banner Contents', {'fields': (
            'banner_color', 'banner_button_one_color', 'banner_button_two_color',
        )}),
        ('Additional Royal Banner Contents', {'fields': (
            'video_title', 'video_description', 'video_url',
        )}),
        ('Gateways and Staffs', {'fields': ('gateways', 'members',)}),
        ('Payments Content', {'fields': ('gateway_title','show_gateways',)}),
        ('Category Content', {'fields': ('category_title','category_subtitle',)}),
        ('Proposal Content', {'fields': ('proposal_title','proposal_subtitle',)}),
        ('Project Content', {'fields': ('project_title','project_subtitle',)}),

        ('Promotion Content', {'fields': (
            'promo_type', 'promo_title','promo_subtitle','promo_description',
            'promo_image','promo_image_tag', 'brand_ambassador_image',
        )}),
        
        ('Social Media', {'fields': (
            'twitter_url', 'instagram_url', 'youtube_url', 'facebook_url',
        )}),
               
    )

    @admin.display(description='Merchant Types', ordering='merchant__user_type')
    def get_user_type(self, obj):
        return obj.merchant.user_type.capitalize()

    @admin.display(description='Merchant', ordering='merchant__first_name')
    def get_merchant(self, obj):
        return obj.merchant.get_full_name()
    
    @admin.display(description='Website', ordering='site')
    def get_site(self, obj):
        return f"Domain: {obj.site.domain} - Name: {obj.site.name}"

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.unregister(Group)

