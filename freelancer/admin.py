from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import Freelancer, FreelancerAction, FreelancerAccount
from .forms import AdminCreditForm
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.utils.html import format_html
from account.fund_exception import FundException

MAX_OBJECTS = 0


class FreelancerAdmin(admin.ModelAdmin):
    model = Freelancer
    list_display = ['image_tag', 'user', 'support', 'hourly_rate', 'tagline']
    list_display_links = ('image_tag', 'user',)    
    readonly_fields = ['image_tag', 'banner_tag','active_team_id']
    search_fields = ('user__short_name','gender','tagline',)
    fieldsets = (
        ('Personal info', {'fields': ('gender', 'hourly_rate', 'address','image_tag', 'profile_photo', 'banner_tag', 'banner_photo',)}),
        ('Interest and Description', {'fields': ('brand_name', 'tagline','description', 'skill', 'business_size', 'department',)}),
        ('Education and Experience #1', {'fields': ('company_name','job_position', 'start_date', 'end_date', 'job_description',)}),
        ('Education and Experience #2', {'fields': ('company_name_two','job_position_two', 'start_date_two', 'end_date_two','job_description_two',)}),
        ('Projects and Awards #1', {'fields': ( 'project_title', 'project_url', 'image_one',)}),
        ('Projects and Awards #2', {'fields': ( 'project_title_two', 'project_url_two', 'image_two',)}),
        ('Projects and Awards #3', {'fields': ( 'project_title_three','project_url_three', 'image_three',)}),
    )    

    radio_fields = {'gender': admin.HORIZONTAL}

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class FreelancerAccountAdmin(admin.ModelAdmin):
    model = FreelancerAccount
    list_display = ['user', 'created_at', 'pending_balance', 'available_balance', 'admin_action']
    readonly_fields = ['user', 'created_at', 'pending_balance', 'available_balance', 'admin_action']
    list_select_related = ('user',)
    
    def get_urls(self):
        urls = super().get_urls()
        pattern = [
            path('<int:account_id>/credit/', self.admin_site.admin_view(self.initiate_memo), name='account-credit'),
        ]
        return pattern + urls


    def admin_action(self, obj):
        return format_html(
            '<a class="button" href="{}"> Initiate Memo</a>',
            reverse('admin:account-credit', args=[obj.pk]),
        )
    
    admin_action.allow_tags = True
    admin_action.short_description = 'Admin Action'

    def initiate_memo(self, request, account_id, *args, **kwargs):
        return self.process_action(
            request=request,
            account_id=account_id,
            action_form=AdminCreditForm,
            action_title='Warning!: If you encounter error like "[Errno 11001] getaddrinfo failed", it means email was not sent to SuperAdmin due to low network from you. But it is possible that memo was initiated so verify first before re-attempting',
        )

    def process_action(self, request, account_id, action_form, action_title):
        account = self.get_object(request, account_id)
        user = request.user
        form = ''
        error_message = ''
        if request.method != 'POST':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                try:
                    form.save(account, user)
                except Exception as e:
                    error_message = str(e)
                    print(error_message)
                    pass
                else:
                    self.message_user(request, 'Successfully initiated memo')
                    url = reverse('admin:freelancer_freelanceraccount_change', args=[account.pk], current_app=self.admin_site.name)
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['account'] = account
        context['title'] = action_title

        return TemplateResponse(request, 'admin/account/admin_credit.html', context)


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
    list_display = ['account','team', 'manager', 'action_choice', 'debit_amount', 'withdraw_amount']
    list_display_links = ['account']
    search_fields = ['team__title', 'position']
    list_filter = ['team']
    readonly_fields = ['account','team', 'manager', 'gateway', 'action_choice','team_staff', 'transfer_status', 'debit_amount', 'withdraw_amount', 'narration','created_at', 'transfer_status']
    list_per_page = 20
    
    fieldsets = (
        ('Background', {'fields': ('account','team', 'manager','action_choice','created_at', 'transfer_status',)}),
        ('Other Transfer Info', {'fields': ('team_staff', 'debit_amount',)}),
        ('Other Withdrawal Info', {'fields': ('gateway', 'withdraw_amount', 'narration',)}),
    )    

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
