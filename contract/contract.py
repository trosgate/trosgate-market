from .models import InternalContract
from django.conf import settings
from general_settings.models import PaymentGateway, DiscountSystem
from general_settings.discount import (
    get_level_one_rate,
    get_level_two_rate, 
    get_level_three_rate, 
    get_level_four_rate,
    get_level_one_start_amount, 
    get_level_one_delta_amount, 
    get_level_two_start_amount, 
    get_level_two_delta_amount, 
    get_level_three_start_amount, 
    get_level_three_delta_amount, 
    get_level_four_start_amount)


class BaseContract():
    """
    This is the base class for contracts
    """
    def __init__(self, request):
        self.session = request.session
        contract_box = self.session.get('contract')
        if 'contract' not in request.session:
            contract_box = self.session['contract'] = {}
        self.contract_box = contract_box

    def capture(self, contract):
        contract_id = str(contract.id)
        chosen_contract = InternalContract.objects.get(pk=contract_id)
        return chosen_contract


    def get_total_price_before_fee_and_discount(self, contract):
        return self.capture(contract).grand_total

    def get_gateway(self):
        if "contractgateway" in self.session:
            return PaymentGateway.objects.get(id=self.session["contractgateway"]["gateway_id"])
        return None

    def get_fee_payable(self):
        newprocessing_fee = 0
        if "contractgateway" in self.session:
            newprocessing_fee = self.get_gateway().processing_fee
        return newprocessing_fee

    def get_discount_value(self, contract):
        discount = 0
        subtotal = self.get_total_price_before_fee_and_discount(contract)

        if (get_level_one_start_amount() <= subtotal <= get_level_one_delta_amount()):
            discount = 0

        if (get_level_two_start_amount() <= subtotal <= get_level_two_delta_amount()):
            discount = ((subtotal * get_level_two_rate())/100)

        if (get_level_three_start_amount() <= subtotal <= get_level_three_delta_amount()):
            discount = ((subtotal * get_level_three_rate())/100)

        if subtotal > get_level_four_start_amount():
            discount = ((subtotal * get_level_four_rate())/100)

        total_discount = round(discount)

        return total_discount


    def get_start_discount_value(self):
        return get_level_two_start_amount()


    def get_discount_multiplier(self, contract):
        subtotal = self.get_total_price_before_fee_and_discount(contract)

        if (get_level_one_start_amount() <= subtotal <= get_level_one_delta_amount()):
            return get_level_one_rate()

        elif (get_level_two_start_amount() <= subtotal <= get_level_two_delta_amount()):
            return get_level_two_rate()

        elif (get_level_three_start_amount() <= subtotal <= get_level_three_delta_amount()):
            return get_level_three_rate()

        elif subtotal > get_level_four_start_amount():
            return get_level_four_rate()
        return 0


    def get_total_price_after_discount_and_fee(self, contract):
        subtotal = self.get_total_price_before_fee_and_discount(contract)
        processing_fee = 0

        if "contractgateway" in self.session:
            processing_fee = self.get_fee_payable()

        grandtotal = ((subtotal - self.get_discount_value(contract)) + processing_fee)
        return grandtotal


    def commit(self):
        self.session.modified = True


    def clean_box(self):
        del self.session['contract']
        del self.session['contractgateway']
        self.commit()
