from django.contrib import admin
from .models import Proposal, OfferContract
from django import forms


class ProposalAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'title', 'team','category', 'created_by', 'salary', 'progress', 'status', 'published']
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ['image_tag', 'title', ]
    list_editable = [ 'status','published']
    search_fields = ['team__title', 'title', 'category__name']
    readonly_fields = ['image_tag']
    actions = ['Go_Public_on_home', 'Go_Private_on_home']
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'slug', 'created_by',)}),
        ('Classification', {'fields': ('team', 'category','reference', 'published',)}),
        ('Description', {'fields': ('description', 'sample_link', 'skill',)}),
        ('FAQs', {'fields': ('faq_one','faq_one_description', 'faq_two', 'faq_two_description', 'faq_three', 'faq_three_description',)}),
        ('Attributes', {'fields': ('salary','service_level', 'revision', 'dura_converter', 'duration','thumbnail',)}),   
    )

    def Go_Public_on_home(self, request, queryset):
        queryset.update(published = True)

    def Go_Private_on_home(self, request, queryset):
        queryset.update(published = False)

    def Go_Private(self, request, queryset):
        queryset.update(published = False)

    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    # def has_delete_permission(self, request, obj=None):
    #     return False


class OfferContractAdmin(admin.ModelAdmin):
    list_display = ['proposal','reference', 'date_created', 'last_updated', 'status', ]
    list_display_links = ['proposal',]
    fieldsets = (
        ('Basic Info', {'fields': ('proposal', 'reference', 'payment_duration','status',)}),
        ('Product/Service #1', {'fields': ('line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',)}),
        ('Product/Service #2', {'fields': ('line_two','line_two_quantity', 'line_two_unit_price', 'line_two_total_price',)}),
        ('Product/Service #3', {'fields': ('line_three','line_three_quantity', 'line_three_unit_price', 'line_three_total_price',)}),
        ('Product/Service #4', {'fields': ('line_four','line_four_quantity', 'line_four_unit_price', 'line_four_total_price',)}),
        ('Notes/Description', {'fields': ('notes', 'date_created','last_updated',)}),       
    )    
    radio_fields = {'payment_duration': admin.HORIZONTAL}
   
   
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


# a class to output datepicker on template
class DateInput(forms.DateInput):
    input_type = 'date'


admin.site.register(OfferContract, OfferContractAdmin)
admin.site.register(Proposal, ProposalAdmin)














