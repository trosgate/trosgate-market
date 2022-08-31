from django.contrib import admin
from .models import Proposal, ProposalChat
from django import forms


class ProposalAdmin(admin.ModelAdmin):
    model = Proposal
    list_display = ['image_tag', 'title', 'team','category', 'salary', 'percent_progress', 'status', 'published']
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ['image_tag', 'title', ]
    list_editable = [ 'status','published']
    search_fields = ['team__title', 'title', 'category__name']
    readonly_fields = ['image_tag']
    actions = ['mark_bulk_to_public', 'mark_bulk_to_private']
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'slug', 'created_by',)}),
        ('Classification', {'fields': ('team', 'category','reference', 'published',)}),
        ('Description', {'fields': ('description', 'sample_link', 'skill',)}),
        ('FAQs', {'fields': ('faq_one','faq_one_description', 'faq_two', 'faq_two_description', 'faq_three', 'faq_three_description',)}),
        ('Attributes', {'fields': ('salary','service_level', 'revision', 'dura_converter', 'thumbnail',)}),   
    )
    

    def mark_bulk_to_public(self, request, queryset):
        queryset.update(published = True)

    def mark_bulk_to_private(self, request, queryset):
        queryset.update(published = False)


    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class ProposalChatAdmin(admin.ModelAdmin):
    model = ProposalChat
    list_display = ['team', 'sender', 'receiver', 'sent_on','content']
    list_display_links = ['team']
    search_fields = ['team']
    list_filter = ['team']



admin.site.register(Proposal, ProposalAdmin)
admin.site.register(ProposalChat, ProposalChatAdmin)














