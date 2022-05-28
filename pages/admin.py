from django.contrib import admin
from .models import TermsAndConditions, Hiring, Freelancing, Sponsorship, Sponsor

MAX_OBJECTS = 1


class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', 'is_published', ]
    list_display_links = ['title', ]
    list_editable = ['is_published', ]
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'slug',)}),
        ('Body Description', {'fields': ('description',)}),
        ('Publish/Hide', {'fields': ('is_published',)}),

    )
    radio_fields = {'is_published': admin.VERTICAL}


class HiringAdmin(admin.ModelAdmin):
    list_display = ['get_howitwork_hiring_tag', 'title',
                    'created_at', 'updated_at', 'is_published', ]
    list_display_links = ['get_howitwork_hiring_tag', 'title', ]
    list_editable = ['is_published', ]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['get_howitwork_hiring_tag']
    fieldsets = (
        ('Basic Info', {
         'fields': ('title', 'subtitle', 'slug', 'is_published',)}),
        ('Body Description', {
         'fields': ('preview', 'backlink', 'thumbnail', 'get_howitwork_hiring_tag')}),

    )
    radio_fields = {'is_published': admin.VERTICAL}


class FreelancingAdmin(admin.ModelAdmin):
    list_display = ['get_howitwork_freelancing_tag', 'title',
                    'created_at', 'updated_at', 'is_published', ]
    list_display_links = ['get_howitwork_freelancing_tag', 'title', ]
    list_editable = ['is_published', ]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['get_howitwork_freelancing_tag']
    fieldsets = (
        ('Basic Info', {
         'fields': ('title', 'subtitle', 'slug', 'is_published',)}),
        ('Body Description', {'fields': (
            'preview', 'backlink', 'thumbnail', 'get_howitwork_freelancing_tag',)}),
        ('Info Option #1', {
         'fields': ('option_one', 'option_one_description',)}),
        ('Info Option #2', {
         'fields': ('option_two', 'option_two_description',)}),
        ('Info Option #3', {
         'fields': ('option_three', 'option_three_description',)}),

    )
    radio_fields = {'is_published': admin.VERTICAL}

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


class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ['get_sponsorship_tag', 'title',
                    'created_at', 'updated_at', 'is_published', ]
    list_display_links = ['get_sponsorship_tag', 'title', ]
    list_editable = ['is_published', ]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['get_sponsorship_tag']
    fieldsets = (
        ('Basic Info', {
         'fields': ('title', 'subtitle', 'slug', 'is_published',)}),
        ('Body Description', {
         'fields': ('preview', 'backlink', 'thumbnail', 'get_sponsorship_tag',)}),

    )
    radio_fields = {'is_published': admin.VERTICAL}


class SponsorsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'availability1',
                    'availability2', 'availability3', 'created_at', ]
    list_display_links = ['name', 'email', ]


admin.site.register(TermsAndConditions, TermsAndConditionsAdmin)
admin.site.register(Hiring, HiringAdmin)
admin.site.register(Freelancing, FreelancingAdmin)
admin.site.register(Sponsorship, SponsorshipAdmin)
admin.site.register(Sponsor, SponsorsAdmin)
