import json 

from django.contrib import admin

from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from . models import (
    NewStats, 
    SuccessProposal, 
    SuccessApplication, 
    SuccessInternalContract,
    UserStatistics
)
from django.db.models import F, Sum, Count, Avg


class NewStatsAdmin(admin.ModelAdmin):
    model = NewStats
    list_display = ['description','win', 'mac', 'iph', 'android','oth']
    list_display_links = ['description']   

    def changelist_view(self, request, extra_context=None):

        stat_data = (
            NewStats.objects.annotate().values("win","mac","iph","android","oth")
        )

        as_json = json.dumps(list(stat_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"stat_data": as_json}

        return super().changelist_view(request, extra_context=extra_context)


    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class SuccessProposalAdmin(admin.ModelAdmin):
    model = SuccessProposal
    list_display = [
        'team', 'created_at','total_sales_price','total_earning', 
        'total_earning_fee_charged', 'total_discount_offered','get_status'
    ]    
    list_display_links = None

    def get_queryset(self, request):
        qs = super(SuccessProposalAdmin, self).get_queryset(request)
        return qs.filter(purchase__status='success')     

    @admin.display(description='Category', ordering='purchase__category')
    def get_status(self, obj):
        return obj.purchase.category   
    
    def changelist_view(self, request, extra_context=None):

        stats_total = SuccessProposal.objects.filter(
            purchase__status='success'
        ).annotate(
            ttotal_sales_price=(F("total_sales_price")),
            ttotal_earning=(F("total_earning")),
            ttotal_earning_fee_charged=(F("total_earning_fee_charged")),
            ttotal_discount_offered=(F("total_discount_offered"))
        ).aggregate(
            total_sales_price=(Sum("ttotal_sales_price")),
            total_earning=(Sum("ttotal_earning")),
            total_earning_fee_charged=(Sum("ttotal_earning_fee_charged")),
            total_discount_offered=(Sum("ttotal_discount_offered"))
        )

        as_json = json.dumps(list(stats_total.values()), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"stat_data": as_json}

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class SuccessContractAdmin(admin.ModelAdmin):
    model = SuccessInternalContract
    list_display = [
        'team', 'created_at','total_sales_price','total_earning', 
        'total_earning_fee_charged', 'total_discount_offered','get_status'
    ]    
    list_display_links = None

    def get_queryset(self, request):
        qs = super(SuccessContractAdmin, self).get_queryset(request)
        return qs.filter(purchase__status='success')     

    @admin.display(description='Category', ordering='purchase__category')
    def get_status(self, obj):
        return obj.purchase.category   
    
    def changelist_view(self, request, extra_context=None):

        stats_total = SuccessInternalContract.objects.filter(
            purchase__status='success'
        ).annotate(
            ttotal_sales_price=(F("total_sales_price")),
            ttotal_earning=(F("total_earning")),
            ttotal_earning_fee_charged=(F("total_earning_fee_charged")),
            ttotal_discount_offered=(F("total_discount_offered"))
        ).aggregate(
            total_sales_price=(Sum("ttotal_sales_price")),
            total_earning=(Sum("total_earning")),
            total_earning_fee_charged=(Sum("ttotal_earning_fee_charged")),
            total_discount_offered=(Sum("ttotal_discount_offered"))
        )

        as_json = json.dumps(list(stats_total.values()), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"stat_data": as_json}

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class SuccessApplicationAdmin(admin.ModelAdmin):
    model = SuccessApplication
    list_display = [
        'team', 'created_at','total_sales_price','total_earning', 
        'total_earning_fee_charged', 'total_discount_offered','get_status'
    ]    
    list_display_links = None

    def get_queryset(self, request):
        qs = super(SuccessApplicationAdmin, self).get_queryset(request)
        return qs.filter(purchase__status='success')     

    @admin.display(description='Category', ordering='purchase__category')
    def get_status(self, obj):
        return obj.purchase.category   
    
    def changelist_view(self, request, extra_context=None):

        stats_total = SuccessApplication.objects.filter(
            purchase__status='success'
        ).annotate(
            ttotal_sales_price=(F("total_sales_price")),
            ttotal_earning=(F("total_earning")),
            ttotal_earning_fee_charged=(F("total_earning_fee_charged")),
            ttotal_discount_offered=(F("total_discount_offered"))
        ).aggregate(
            total_sales_price=(Sum("ttotal_sales_price")),
            total_earning=(Sum("total_earning")),
            total_earning_fee_charged=(Sum("ttotal_earning_fee_charged")),
            total_discount_offered=(Sum("ttotal_discount_offered"))
        )

        as_json = json.dumps(list(stats_total.values()), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"stat_data": as_json}

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class UserStatisticsAdmin(admin.ModelAdmin):
    model = UserStatistics
    list_display = ['short_name', 'country','user_type', 'is_active', 'is_staff', 'is_assistant', 'is_superuser', 'date_joined','last_login']   
    search_fields = ('email', 'first_name', 'last_name',)
    list_display_links = None
       
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(NewStats, NewStatsAdmin)
admin.site.register(SuccessProposal, SuccessProposalAdmin)
admin.site.register(SuccessApplication, SuccessApplicationAdmin)
admin.site.register(SuccessInternalContract, SuccessContractAdmin)
admin.site.register(UserStatistics, UserStatisticsAdmin)
