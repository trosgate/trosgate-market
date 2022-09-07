from django.contrib import admin
from .models import PaymentAccount, PaymentRequest, AdminCredit
from django.db import transaction as db_transaction
from .forms import AdminApproveForm, PaymentChallengeForm
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.http import HttpResponseRedirect



@admin.register(PaymentAccount)
class PaymentAccountAdmin(admin.ModelAdmin):
    model = PaymentAccount
    list_display = ['user', 'created_at']
    readonly_fields = ['created_at',]
    list_display_links = ['user',]

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    model = PaymentRequest
    list_display = [ 'reference', 'gateway', 'amount','payday', 'status', 'admin_action']
    readonly_fields = ['team', 'status','user','gateway', 'message', 'amount', 'created_at', 'payday', 'reference', 'admin_action']
    list_display_links = ('reference',)
    list_filter=['status']
    actions = ['mark_paid_in_single_or_bulk']

    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def mark_paid_in_single_or_bulk(self, request, queryset):
        with db_transaction.atomic():
            for query in queryset:
                PaymentRequest.mark_paid(query.pk)
        self.message_user(request, 'Successfully executed the bulk operation and mail send to respective users')
        queryset.update(status = True)
 
    def get_urls(self):
        urls = super().get_urls()
        pattern = [
            path('<int:payout_id>/message/', self.admin_site.admin_view(self.payout_challenge), name='payout-challenge'),
        ]
        return pattern + urls


    def admin_action(self, obj):
        return format_html(
            '<a class="button" href="{}"> Declined Mail</a>',
            reverse('admin:payout-challenge', args=[obj.pk]),
        )
    
    admin_action.allow_tags = True
    admin_action.short_description = 'Admin Action'

    def payout_challenge(self, request, payout_id, *args, **kwargs):
        return self.process_action(
            request=request,
            payout_id=payout_id,
            action_form=PaymentChallengeForm,
            action_title='This email will go to withdrawal Initiator',
        )

    def process_action(self, request, payout_id, action_form, action_title):
        payout = self.get_object(request, payout_id)
        form = ''
        error_message = ''
        if request.method != 'POST':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                try:
                    form.save(payout.id, payout.message)
                except Exception as e:
                    error_message = str(e)
                    print(error_message)
     
                    pass
                else:
                    self.message_user(request, 'Successfully sent mail to user')
                    url = reverse('admin:payments_paymentrequest_change', args=[payout.pk], current_app=self.admin_site.name)
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['payout'] = payout
        context['title'] = action_title

        return TemplateResponse(request, 'admin/account/admin_credit.html', context)


@admin.register(AdminCredit)
class AdminCreditAdmin(admin.ModelAdmin):
    model = AdminCredit
    list_display = [ 'reference', 'sender', 'team', 'amount', 'created_at', 'status', 'admin_action']
    readonly_fields = ['sender', 'receiver', 'reference', 'team', 'amount', 'status', 'comment', 'created_at']
    list_display_links = ['sender','amount']
    list_per_page = 20

    fieldsets = (
        ('Details of Memo', {'fields': ('sender', 'receiver', 'reference', 'team', 'amount', 'comment','created_at',)}),
        ('Change Status to Approve', {'fields': ( 'status',)}),
    )


    def get_urls(self):
        urls = super().get_urls()
        pattern = [
            path('<int:account_id>/approve/', self.admin_site.admin_view(self.approve_memo), name='approve-memo'),
        ]
        return pattern + urls


    def admin_action(self, obj):
        return format_html(
            '<a class="button" href="{}"> Approve Memo</a>',
            reverse('admin:approve-memo', args=[obj.pk]),
        )
    
    admin_action.allow_tags = True
    admin_action.short_description = 'Admin Action'

    def approve_memo(self, request, account_id, *args, **kwargs):
        return self.process_action(
            request=request,
            account_id=account_id,
            action_form=AdminApproveForm,
            action_title='About to give credit. Action is irreversible so be sure',
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
                    self.message_user(request, 'Successfully approved memo')
                    url = reverse('admin:payments_admincredit_change', args=[account.pk], current_app=self.admin_site.name)
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['account'] = account
        context['title'] = action_title

        return TemplateResponse(request, 'admin/account/admin_credit_approve.html', context)


    def has_add_permission(self, request):        
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions










