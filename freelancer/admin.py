from django.contrib import admin
from . models import Freelancer, FreelancerAction, FreelancerAccount

MAX_OBJECTS = 0

class FreelancerAdmin(admin.ModelAdmin):
    model = Freelancer
    list_display = ['image_tag', 'user', 'support', 'hourly_rate', 'tagline']
    list_display_links = ('image_tag', 'user',)    
    readonly_fields = ['image_tag', 'banner_tag','active_team_id']
    search_fields = ('user__short_name','gender','tagline',)
    fieldsets = (
        ('Personal info', {'fields': ('gender', 'hourly_rate', 'address','image_tag', 'profile_photo', 'banner_tag', 'banner_photo',)}),
        ('Interest and Description', {'fields': ('brand_name', 'tagline','description','business_size', 'department',)}),
        ('Education and Experience #1', {'fields': ('company_name','job_position', 'start_date', 'end_date', 'job_description',)}),
        ('Education and Experience #2', {'fields': ('company_name_two','job_position_two', 'start_date_two', 'end_date_two','job_description_two',)}),
        ('Projects and Awards #1', {'fields': ( 'project_title', 'project_url', 'image_one',)}),
        ('Projects and Awards #2', {'fields': ( 'project_title_two', 'project_url_two', 'image_two',)}),
        ('Projects and Awards #3', {'fields': ( 'project_title_three','project_url_three', 'image_three',)}),
        ('Number of Teams', {'fields': ( 'active_team_id',)}),
    )    

    radio_fields = {'gender': admin.HORIZONTAL}

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class FreelancerAccountAdmin(admin.ModelAdmin):
    model = FreelancerAccount
    list_display = ['user', 'created_at','reference', 'available_balance']
    list_editable = ['available_balance']
    list_display_links = None

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


class FreelancerActionAdmin(admin.ModelAdmin):
    model = FreelancerAction    
    list_display = ['account','team', 'manager', 'action_choice','team_staff','position', 'transfer_status', 'debit_amount', 'withdraw_amount']
    list_display_links = None
    search_fields = ['team__title', 'position']
    list_filter = ['team']

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

admin.site.register(Freelancer, FreelancerAdmin)
admin.site.register(FreelancerAccount, FreelancerAccountAdmin)
admin.site.register(FreelancerAction, FreelancerActionAdmin)