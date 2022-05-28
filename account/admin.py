from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Customer, Country, TwoFactorAuth
from django.utils.translation import gettext_lazy as _
import sys


class CustomerCreationForm(forms.ModelForm):

    # ADMIN = 'admin'
    # USER_TYPE = (
    #     (ADMIN, _('Admin')),
    # )    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    # user_type = forms.ChoiceField(required=True, choices=USER_TYPE, label="Select Type")

    class Meta:
        model = Customer
        fields = ('email', 'user_type', 'short_name',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomerChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Customer
        fields = ['email', 'short_name', 'country', 'password', 'is_active', 'is_admin']

    def clean_password(self):
        return self.initial['password']


class CustomerAdmin(BaseUserAdmin,):
    model = Customer    
    form = CustomerChangeForm
    add_form = CustomerCreationForm

    list_display = ['email', 'short_name', 'country','user_type', 'is_active', 'is_staff', 'is_admin']
    readonly_fields = ['date_joined', 'user_type', 'last_login']  # , 'is_active'
    list_display_links = ['email','short_name']
    list_filter = ['user_type', 'is_admin', 'is_staff']
    fieldsets = (
        ('Personal Information', {'fields': ('email', 'short_name', 'first_name', 'last_name', 'phone', 'country', 'password',)}),
        ('User Type', {'fields': ('user_type',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin',)}),
        ('Activity Log', {'fields': ('date_joined', 'last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',) #'user_type', 
        }),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)
    filter_horizontal = ()
    list_per_page = 10

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return True


class CountryAdmin(admin.ModelAdmin):
    model = Country
    list_display = ['flag_tag', 'name',
                    'country_code', 'ordering', 'supported']
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


class TwoFactorAuthAdmin(admin.ModelAdmin):
    model = TwoFactorAuth    
    list_display = ['user', 'last_login', 'pass_code']
    readonly_fields = ['last_login']      

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(TwoFactorAuth, TwoFactorAuthAdmin)
admin.site.unregister(Group)
