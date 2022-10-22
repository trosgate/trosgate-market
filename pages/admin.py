from django.contrib import admin
from .models import TermsAndConditions, Hiring, Freelancing, AboutUsPage, Investor

MAX_OBJECTS = 1
HIRING_MAX_OBJECTS = 4


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    model=TermsAndConditions
    list_display = ['title', 'created_at', 'updated_at', 'is_published', ]
    list_display_links = ['title', ]
    list_editable = ['is_published', ]
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'slug',)}),
        ('Body Description', {'fields': ('quote', 'description',)}),
        ('Publish/Hide', {'fields': ('is_published',)}),

    )
    radio_fields = {'is_published': admin.VERTICAL}


@admin.register(Hiring)
class HiringAdmin(admin.ModelAdmin):
    model=Hiring
    list_display = ['get_howitwork_hiring_tag', 'title',
                    'updated_at', 'ordering', 'is_published', ]
    list_display_links = ['get_howitwork_hiring_tag', 'title', ]
    list_editable = ['ordering', 'is_published', ]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['get_howitwork_hiring_tag']
    fieldsets = (
        ('Basic Info', {
         'fields': ('title', 'subtitle', 'slug', 'is_published',)}),
        ('Body Description', {
         'fields': ('preview', 'backlink', 'thumbnail', 'get_howitwork_hiring_tag')}),

    )
    radio_fields = {'is_published': admin.VERTICAL}

    def has_add_permission(self, request):
        if self.model.objects.count() >= HIRING_MAX_OBJECTS:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Freelancing)
class FreelancingAdmin(admin.ModelAdmin):
    model=Freelancing
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
        ('Getting Hired via Proposals', {
         'fields': ('option_one', 'option_one_description',)}),
        ('Getting Hired via Contracts', {
         'fields': ('option_two', 'option_two_description',)}),
        ('Getting Hired via Projects', {
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


@admin.register(AboutUsPage)
class AboutUsPageAdmin(admin.ModelAdmin):
    model=AboutUsPage
    list_display = ['title', 'subtitle']
    list_display_links = ['title', 'subtitle']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at',]
    fieldsets = (
        ('About Info', {
         'fields': ('title', 'subtitle', 'slug', 'description',)}),
        ('About Media ', {
         'fields': ('banner_type', 'video_url', 'ad_image', 'display_stats',)}),
        ('Hero Banner Attributes ', {
         'fields': ('title_block', 'subtitle_block', 'banner_image','banner_color', 'banner_button_one_color', 'banner_button_two_color')}),
        ('Logger', {
         'fields': ('created_at', 'updated_at',)}),

    )
    radio_fields = {'banner_type': admin.HORIZONTAL}

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


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    model=Investor
    list_display = ['id', 'salutation', 'myname', 'myemail', 'created_at', 'verified']
    list_display_links = None
    readonly_fields = ['salutation', 'myname', 'myemail', 'created_at', 'updated_at', 'verified']
    
    def has_add_permission(self, request): 
        return False

