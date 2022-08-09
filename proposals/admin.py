from django.contrib import admin
from .models import Proposal, ProposalChat
from django import forms


class ProposalAdmin(admin.ModelAdmin):
    model = Proposal
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
        ('Attributes', {'fields': ('salary','service_level', 'revision', 'dura_converter', 'thumbnail',)}),   
    )

    def Go_Public_on_home(self, request, queryset):
        # # query = queryset
        # # for query in queryset:
        # print('queryset Pk:', queryset, 'queryset title:', queryset)
        queryset.update(published = True)

    def Go_Private_on_home(self, request, queryset):
        queryset.update(published = False)

    def Go_Private(self, request, queryset):
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














