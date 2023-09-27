from .models import Contract
from django.conf import settings
from payments.models import PaymentGateway
from general_settings.models import DiscountSystem
from general_settings.discount import (
    get_level_one_rate, get_level_two_rate, get_level_three_rate, 
    get_level_four_rate, get_level_one_start_amount, get_level_one_delta_amount, 
    get_level_two_start_amount, get_level_two_delta_amount, get_level_three_start_amount, 
    get_level_three_delta_amount, get_level_four_start_amount
)
import math

class BaseContract():
    """
    This is the base class for contracts
    """
    def __init__(self, request):
        self.session = request.session
        contract_box = self.session.get(settings.CONTRACT_SESSION_ID)
        if settings.CONTRACT_SESSION_ID not in request.session:
            contract_box = self.session[settings.CONTRACT_SESSION_ID] = {}
        self.contract_box = contract_box

    def capture(self, contract):
        contract_id = str(contract.id)
        chosen_contract = Contract.objects.filter(pk=contract_id).first()
        
        if "chosencontract" not in self.session:
            self.session["chosencontract"] = {"contract_id": contract.id}
        else:
            self.session["chosencontract"]["contract_id"] = contract.id

        self.commit()
        return chosen_contract

    def get_total_price_before_fee_and_discount(self, contract):
        return self.capture(contract).grand_total

    def get_gateway(self):
        if settings.CONTRACT_GATEWAY_SESSION_ID in self.session:
            return PaymentGateway.objects.get(id=self.session[settings.CONTRACT_GATEWAY_SESSION_ID]["gateway_id"])
        return None

    def get_fee_payable(self):
        newprocessing_fee = 0
        if settings.CONTRACT_GATEWAY_SESSION_ID in self.session:
            newprocessing_fee = self.get_gateway().processing_fee
        return newprocessing_fee


    def get_discount_value(self, contract):
        discount = 0
        subtotal = self.get_total_price_before_fee_and_discount(contract)

        if (get_level_one_start_amount() <= subtotal <= get_level_one_delta_amount()):
            discount = 0

        elif (get_level_two_start_amount() <= subtotal <= get_level_two_delta_amount()):
            discount = ((subtotal * get_level_two_rate())/100)
        elif (get_level_three_start_amount() <= subtotal <= get_level_three_delta_amount()):
            discount = ((subtotal * get_level_three_rate())/100)

        elif subtotal > get_level_four_start_amount():
            discount = ((subtotal * get_level_four_rate())/100)

        return round(discount)


    def get_start_discount_value(self):
        return get_level_two_start_amount()

    def get_discount_multiplier(self, contract):
        subtotal = self.get_total_price_before_fee_and_discount(contract)
        rate = 0
        if (get_level_one_start_amount() <= subtotal <= get_level_one_delta_amount()):
            rate = get_level_one_rate()

        elif (get_level_two_start_amount() <= subtotal <= get_level_two_delta_amount()):
            rate = get_level_two_rate()

        elif (get_level_three_start_amount() <= subtotal <= get_level_three_delta_amount()):
            rate = get_level_three_rate()

        elif subtotal > get_level_four_start_amount():
            rate = get_level_four_rate()
        return rate

    def get_total_price_after_discount_and_fee(self, contract):
        subtotal = self.get_total_price_before_fee_and_discount(contract)
        processing_fee = 0

        if settings.CONTRACT_GATEWAY_SESSION_ID in self.session:
            processing_fee = self.get_fee_payable()

        grandtotal = ((subtotal - self.get_discount_value(contract)) + processing_fee)
        return grandtotal

    def commit(self):
        self.session.modified = True

    def clean_box(self):
        del self.session[settings.CONTRACT_SESSION_ID]
        del self.session[settings.CONTRACT_GATEWAY_SESSION_ID]
        self.commit()
