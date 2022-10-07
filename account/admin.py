from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Customer, Country, TwoFactorAuth
from django.utils.translation import gettext_lazy as _
import sys


MAX_OBJECTS = 0

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


class CustomerAdmin(BaseUserAdmin,):
    model = Customer    
    form = CustomerChangeForm
    add_form = CustomerCreationForm

    list_display = ['id', 'short_name', 'email', 'country','user_type', 'is_active', 'last_login']
    readonly_fields = ['date_joined', 'user_type', 'last_login']
    list_display_links = ['short_name']
    list_filter = ['user_type', 'is_superuser', 'is_assistant',]
    fieldsets = (
        ('Personal Information', {'fields': ('email', 'short_name', 'first_name', 'last_name', 'phone', 'country', 'password',)}),
        ('All User Permissions', {'fields': ('user_type','is_active','is_staff',)}),
        ('Company Roles', {'fields': ('is_assistant', 'is_superuser',)}),
        ('Activity Log', {'fields': ('date_joined', 'last_login',)}),
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
            return qs.filter(pk=request.user.id)  

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

        if obj is not None and not obj.is_staff: # Means object is freelancer or client
            disabled_fields |= {                
                'is_superuser',
                'is_staff',
                'is_assistant',
            }


        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True
        
        return form


class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display = ['flag_tag', 'name', 'country_code', 'ordering', 'supported']
    readonly_fields = ['flag_tag']
    list_display_links = ['flag_tag', 'name']
    list_editable = ['ordering', 'supported']
    radio_fields = {'supported': admin.HORIZONTAL}
    actions = ['Activate_Countries', 'Deactivate_Countries']
    search_fields = ('name', 'country_code',)
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


# class TwoFactorAuthAdmin(admin.ModelAdmin):
#     model = TwoFactorAuth    
#     list_display = ['user', 'get_user_type', 'last_login', 'pass_code']
#     readonly_fields = ['user', 'last_login', 'pass_code']     
#     list_display_links = None

#     def get_queryset(self, request):
#         qs = super(TwoFactorAuthAdmin, self).get_queryset(request)
#         if request.user.is_superuser:
#             return qs.all()  
#         else:
#             return qs.filter(pk=0)  
            
#     @admin.display(description='User Types', ordering='user__user_type')
#     def get_user_type(self, obj):
#         return obj.user.user_type

#     def has_add_permission(self, request):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_actions(self, request):
#         actions = super().get_actions(request)

#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Country, CountryAdmin)
# admin.site.register(TwoFactorAuth, TwoFactorAuthAdmin)
admin.site.unregister(Group)
