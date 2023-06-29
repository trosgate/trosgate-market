from django.contrib import admin
from .models import Proposal, ProposalSupport, ProposalChat
from django import forms


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'title', 'team','category', 'salary', 'status', 'published']
    list_display_links = ['image_tag', 'title']
    list_editable = [ 'status','published']
    search_fields = ['team__title', 'title', 'category__name']
    readonly_fields = [
        'created_by','image_tag', 'sample_link', 'skill','description',
        'team', 'category','reference', 'published', 'faq_three', 'faq_three_description',
        'faq_one','faq_one_description', 'faq_two', 'faq_two_description', 'identifier', 
        'salary','service_level', 'revision', 'dura_converter', 'thumbnail','merchant'
    ]
    actions = ['mark_bulk_to_public', 'mark_bulk_to_private']
    fieldsets = (
        ('Basic Info', {'fields': ('created_by','merchant','team', 'identifier',)}),
        ('Product pricing', {'fields': ('digital', 'tier_pricing','salary', 'salary_tier1','salary_tier2', 'salary_tier3',)}),
        ('Classification', {'fields': ('category','reference', 'published',)}),
        ('Description', {'fields': ('description', 'sample_link', 'skill',)}),
        ('FAQs', {'fields': ('faq_one','faq_one_description', 'faq_two', 'faq_two_description', 'faq_three', 'faq_three_description',)}),
        ('Attributes', {'fields': ('service_level', 'revision', 'dura_converter', 'thumbnail',)}),   
    )
    
    def mark_bulk_to_public(self, request, queryset):
        queryset.update(published = True)

    def mark_bulk_to_private(self, request, queryset):
        queryset.update(published = False)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ProposalSupportInline(admin.StackedInline):
    model = ProposalChat
    list_display = ['merchant', 'team', 'sender', 'sent_on']
    readonly_fields = ['merchant','team', 'sender', 'sent_on','content']
    extra = 0

    fieldsets = (
        ('Comment Thread', {'fields': ('content', 'sent_on',)}),
    )


    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(ProposalSupport)
class ProposalSupportAdmin(admin.ModelAdmin):
    model = ProposalSupport
    list_display = ['merchant', 'team', 'title', 'created_at']
    list_display_links = ['merchant', 'team','title',]
    readonly_fields = ['merchant', 'team', 'title', 'created_at']
    search_fields = ['team__title', 'title']

    fieldsets = (
        ('Proposal Info', {'fields': ('merchant', 'team', 'title',)}),
    )
    inlines = [ProposalSupportInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions















