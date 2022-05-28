from general_settings.models import PaymentAPI
from django.shortcuts import get_object_or_404
from proposals.models import Proposal
from freelancer.models import Freelancer, FundTransfer
from orders.models import Order, OrderItem


class Algorithm():

    def __init__(self, team):
        """
        An algorithm for dynamically splitting each proposal sales value into shares and updating balance
        """
        self.team = team


    def shares(self, team, staff):
        """
        An algorithm for dynamically returning a scenario shares calculation
        """
        try:
            fees = PaymentAPI.objects.get(id=1)

            admin_fee = fees.proposal_fee  

            team = team

            subtotal = 500

            admin_fees_percent = (admin_fee/100)

            admin_fees_amount = round(subtotal * admin_fees_percent)

            payable_amount = subtotal - admin_fees_amount

            member_balance = sum(split.salary for split in FundTransfer.objects.filter(team=team, staff=staff))

            balance = ((member_balance/100) * payable_amount)

            return balance

        except:
            print("something went wrong")

