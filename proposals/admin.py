from django.contrib import admin
from .models import Proposal, ProposalSupport, ProposalChat
from django import forms


class ProposalAdmin(admin.ModelAdmin):
    model = Proposal
    list_display = ['image_tag', 'title', 'team','category', 'salary', 'percent_progress', 'status', 'published']
    list_display_links = ['image_tag', 'title']
    list_editable = [ 'status','published']
    search_fields = ['team__title', 'title', 'category__name']
    readonly_fields = [
        'created_by','image_tag','description', 'sample_link', 'skill',
        'team', 'category','reference', 'published', 'faq_three', 'faq_three_description',
        'faq_one','faq_one_description', 'faq_two', 'faq_two_description', 
        'salary','service_level', 'revision', 'dura_converter', 'thumbnail',
    ]
    actions = ['mark_bulk_to_public', 'mark_bulk_to_private']
    fieldsets = (
        ('Basic Info', {'fields': ('created_by',)}),
        ('Classification', {'fields': ('team', 'category','reference', 'published',)}),
        ('Description', {'fields': ('description', 'sample_link', 'skill',)}),
        ('FAQs', {'fields': ('faq_one','faq_one_description', 'faq_two', 'faq_two_description', 'faq_three', 'faq_three_description',)}),
        ('Attributes', {'fields': ('salary','service_level', 'revision', 'dura_converter', 'thumbnail',)}),   
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


# class ProposalSupportInline(admin.StackedInline):
#     model = ProposalChat
#     list_display = ['team', 'sender', 'sent_on']
#     readonly_fields = ['team', 'sender', 'sent_on','content']
#     extra = 0

#     fieldsets = (
#         ('Reply Messages', {'fields': ('content', 'sent_on',)}),
#     )


#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_actions(self, request):
#         actions = super().get_actions(request)

#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions


# class ProposalSupportAdmin(admin.ModelAdmin):
#     model = ProposalSupport
#     list_display = ['team', 'title', 'created_at']
#     list_display_links = ['team','title',]
#     readonly_fields = ['team', 'title']
#     search_fields = ['team__title', 'title']

#     fieldsets = (
#         ('Proposal Info', {'fields': ('team', 'title',)}),
#     )
#     inlines = [ProposalSupportInline]

#     def has_add_permission(self, request):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_actions(self, request):
#         actions = super().get_actions(request)

#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions


admin.site.register(Proposal, ProposalAdmin)
# admin.site.register(ProposalSupport, ProposalSupportAdmin)














