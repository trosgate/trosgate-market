from django.contrib import admin
from .models import Contractor, Contract, InternalContract, ContractChat, InternalContractChat


class ContractorAdmin(admin.ModelAdmin):
    model = Contractor
    list_display = ['name',  'email', 'team', 'created_by', 'date_created']
    list_display_links = ['name', 'created_by',]
    readonly_fields = [
        'name',  'email', 'team', 'created_by', 'date_created', 
        'phone_Number','address','postal_code'
        ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ContractAdmin(admin.ModelAdmin):
    list_display = ['client', 'team', 'reference', 'contract_duration', 'grand_total', 'reaction']
    list_display_links = ['client', 'team']
    readonly_fields = [
        'team', 'created_by', 'client', 'reference', 'contract_duration', 'reaction', 'slug',
        'line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',
        'line_two','line_two_quantity', 'line_two_unit_price', 'line_two_total_price',
        'line_three','line_three_quantity', 'line_three_unit_price', 'line_three_total_price',
        'line_four','line_four_quantity', 'line_four_unit_price', 'line_four_total_price',
        'line_five','line_five_quantity', 'line_five_unit_price', 'line_five_total_price',
        'notes', 'date_created','last_updated','grand_total',
        ]
    # list_editable = ['reaction']

    fieldsets = (
        ('Basic Info', {'fields': ('team', 'created_by', 'client', 'contract_duration','reaction','slug','reference',)}),
        ('Service Description #1', {'fields': ('line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',)}),
        ('Service Description #2', {'fields': ('line_two','line_two_quantity', 'line_two_unit_price', 'line_two_total_price',)}),
        ('Service Description #3', {'fields': ('line_three','line_three_quantity', 'line_three_unit_price', 'line_three_total_price',)}),
        ('Service Description #4', {'fields': ('line_four','line_four_quantity', 'line_four_unit_price', 'line_four_total_price',)}),
        ('Service Description #5', {'fields': ('line_five','line_five_quantity', 'line_five_unit_price', 'line_five_total_price',)}),
        ('Notes/Description', {'fields': ('notes', 'date_created','last_updated','grand_total',)}),
       
    )    
    radio_fields = {'contract_duration': admin.HORIZONTAL}


    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class InternalContractAdmin(admin.ModelAdmin):
    list_display = ['team','reference', 'get_proposal_title', 'grand_total', 'reaction']
    list_display_links = ['team','reference']
    search_fields = ['team__title', 'proposal__title']
    readonly_fields = [
        'team', 'created_by', 'reference', 'proposal', 'contract_duration','reaction','slug',
        'line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',
        'line_two','line_two_quantity', 'line_two_unit_price', 'line_two_total_price',
        'line_three','line_three_quantity', 'line_three_unit_price', 'line_three_total_price',
        'line_four','line_four_quantity', 'line_four_unit_price', 'line_four_total_price',
        'line_five','line_five_quantity', 'line_five_unit_price', 'line_five_total_price',
        'notes', 'date_created','last_updated','grand_total',
        ]

    fieldsets = (
        ('Basic Info', {'fields': ('team', 'created_by', 'proposal', 'contract_duration','reaction','slug','reference',)}),
        ('Service Description #1', {'fields': ('line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',)}),
        ('Service Description #2', {'fields': ('line_two','line_two_quantity', 'line_two_unit_price', 'line_two_total_price',)}),
        ('Service Description #3', {'fields': ('line_three','line_three_quantity', 'line_three_unit_price', 'line_three_total_price',)}),
        ('Service Description #4', {'fields': ('line_four','line_four_quantity', 'line_four_unit_price', 'line_four_total_price',)}),
        ('Service Description #5', {'fields': ('line_five','line_five_quantity', 'line_five_unit_price', 'line_five_total_price',)}),
        ('Notes/Description', {'fields': ('notes', 'date_created','last_updated','grand_total',)}),
       
    )    
    radio_fields = {'contract_duration': admin.HORIZONTAL}

    @admin.display(description='Proposal', ordering='proposal__title')
    def get_proposal_title(self, obj):
        return obj.proposal.title


    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


# class ContractChatInline(admin.StackedInline):
#     list_display = ['team','sender','sent_on']
#     readonly_fields = ['team','sender','sent_on','content']
#     model = ContractChat
#     extra = 0
#     fieldsets = (
#         ('Reply Messages', {'fields': ('sender', 'content', 'sent_on',)}),
#     )


# class InternalContractChatAdmin(admin.ModelAdmin):
#     list_display = ['team', 'get_proposal_title', 'date_created']
#     readonly_fields = ['team','created_by', 'date_created']
#     fieldsets = (
#         ('Contract Parties', {'fields': ['created_by', 'team', 'date_created'],}),
#     )
#     inlines = [ContractChatInline]

#     class Meta:
#         model = InternalContractChat 

#     def has_add_permission(self, request):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False

#     def get_actions(self, request):
#         actions = super().get_actions(request)

#         if 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions

#     @admin.display(description='Proposal', ordering='proposal__title')
#     def get_proposal_title(self, obj):
#         return obj.proposal.title


admin.site.register(Contract, ContractAdmin)
admin.site.register(InternalContract, InternalContractAdmin)
admin.site.register(Contractor, ContractorAdmin)
# admin.site.register(InternalContractChat, InternalContractChatAdmin)

