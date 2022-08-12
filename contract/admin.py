from django.contrib import admin
from .models import Contractor, Contract, InternalContract, ContractChat, InternalContractChat


class ContractorAdmin(admin.ModelAdmin):
    model = Contractor
    list_display = ['name', 'team', 'email', 'reference', 'date_created']
    list_display_links = ['name', 'reference',]
    exclude = ('reference',)


class ContractAdmin(admin.ModelAdmin):
    list_display = ['client','team', 'reference', 'date_created', 'grand_total', 'status', ]
    readonly_fields = ['last_updated','date_created']
    list_display_links = ['client',]
    exclude = ('created_by', 'reference',)
    fieldsets = (
        ('Basic Info', {'fields': ('team', 'client', 'contract_duration','status','slug',)}),
        ('Service Description #1', {'fields': ('line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',)}),
        ('Service Description #2', {'fields': ('line_two','line_two_quantity', 'line_two_unit_price', 'line_two_total_price',)}),
        ('Service Description #3', {'fields': ('line_three','line_three_quantity', 'line_three_unit_price', 'line_three_total_price',)}),
        ('Service Description #4', {'fields': ('line_four','line_four_quantity', 'line_four_unit_price', 'line_four_total_price',)}),
        ('Service Description #5', {'fields': ('line_five','line_five_quantity', 'line_five_unit_price', 'line_five_total_price',)}),
        ('Notes/Description', {'fields': ('notes', 'date_created','last_updated', 'grand_total',)}),
       
    )    
    radio_fields = {'contract_duration': admin.HORIZONTAL}


class InternalContractAdmin(admin.ModelAdmin):
    list_display = ['team', 'proposal', 'grand_total', 'reaction']
    list_display_links = ['team',]
    readonly_fields = ['last_updated','created_by', 'date_created']
    list_editable = ['reaction']
    exclude = ('created_by', 'reference',)
    fieldsets = (
        ('Basic Info', {'fields': ('team', 'created_by', 'proposal', 'contract_duration','reaction','slug',)}),
        ('Service Description #1', {'fields': ('line_one','line_one_quantity', 'line_one_unit_price', 'line_one_total_price',)}),
        ('Service Description #2', {'fields': ('line_two','line_two_quantity', 'line_two_unit_price', 'line_two_total_price',)}),
        ('Service Description #3', {'fields': ('line_three','line_three_quantity', 'line_three_unit_price', 'line_three_total_price',)}),
        ('Service Description #4', {'fields': ('line_four','line_four_quantity', 'line_four_unit_price', 'line_four_total_price',)}),
        ('Service Description #5', {'fields': ('line_five','line_five_quantity', 'line_five_unit_price', 'line_five_total_price',)}),
        ('Notes/Description', {'fields': ('notes', 'date_created','last_updated','grand_total',)}),
       
    )    
    radio_fields = {'contract_duration': admin.HORIZONTAL}

class ContractChat(admin.TabularInline):
    # readonly_fields = ['team','sender','content']
    model = ContractChat
    extra = 0
    # can_delete = False

class InternalContractChatAdmin(admin.ModelAdmin):
    list_display = ['team', 'proposal']
    readonly_fields = ['team','created_by']
    fieldsets = (
        ('Contract Parties', {'fields': ['created_by', 'team'],}),
    )
    inlines = [ContractChat]


    class Meta:
        model = InternalContractChat 

admin.site.register(InternalContract, InternalContractAdmin)
admin.site.register(Contractor, ContractorAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(InternalContractChat, InternalContractChatAdmin)

