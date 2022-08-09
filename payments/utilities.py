from transactions.models import ApplicationSale, Purchase, ProposalSale, ContractSale
from .models import PaymentRequest
from django.dispatch import receiver


# def credit_team_founder_pending_balance(purchase_id:int):
#     if ProposalSale.objects.filter(purchase__id=purchase_id, purchase__status='success').exists():
#         for item in ProposalSale.objects.filter(purchase__id=purchase_id, purchase__status='success'):
#             founder_account = item.team.created_by.fundtransferuser
#             # founder_account.pending_balance += sum([item.total_earning])
#             print('balance:::', founder_account.pending_balance)
#             founder_account.save()
















