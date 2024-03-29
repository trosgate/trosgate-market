from proposals.models import Proposal
from payments.models import PaymentGateway
from general_settings.models import DiscountSystem
from django.conf import settings
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


class HiringBox():
    """
    This is the base class for proposal hiring sessions
    """
    def __init__(self, request):
        self.session = request.session
        hiring_box = self.session.get(settings.HIRINGBOX_SESSION_ID)
        if settings.HIRINGBOX_SESSION_ID not in request.session:
            hiring_box = self.session[settings.HIRINGBOX_SESSION_ID] = {}
        self.hiring_box = hiring_box


    def set_pricing(self, proposal, package_name, package_price):
        self.session['selected_package'] = {
            'id': proposal,
            'package_name': package_name,
            'package_price': package_price
        }
    
    def get_pricing(self):
        return self.session.get('selected_package')


    def addon(self, proposal, member_qty, salary, package_name):
        """
        Apply to proposals excluding digital product
        This function will add proposal to session at its original price
        This function will modify proposal by updating member quantity that client wishes to hire
        """
        proposal_id = str(proposal.id)
        if proposal_id in self.hiring_box:
            self.hiring_box[proposal_id]["member_qty"] = member_qty
            self.hiring_box[proposal_id]["salary"] = salary
            self.hiring_box[proposal_id]["package_name"] = package_name
        else:
            self.hiring_box[proposal_id] = {'salary': int(salary), 'package_name': package_name, 'member_qty': int(member_qty)}
        self.commit()


    def add_product(self, product):
        proposal_session = product.id
        if proposal_session in self.hiring_box:
            self.hiring_box[proposal_session]["product_id"] = product.id
            self.hiring_box[proposal_session]["price"] = product.price
        else:
            self.hiring_box[proposal_session] = {'product_id': product.id, 'price': int(product.price)}
        self.commit()


    # def get_products_price(self):
    #     return self.get_p['price']

    def modify(self, proposal, member_qty, price):
        """
        We grab the proposal as a string, 
        then On condition that we have proposal in session at its original price,
        This function will modify proposal by updating members quantity that client wishes to hire
        """
        proposal_id = str(proposal)

        if proposal_id in self.hiring_box:
            self.hiring_box[proposal_id]["member_qty"] = member_qty
            self.hiring_box[proposal_id]["salary"] = price
        else:
            self.hiring_box[proposal_id] = {"salary": int(price), "member_qty": int(member_qty)}
        self.commit()


    def __iter__(self):
        """
        Collect the proposal_id in the session data to query the database
        and return iterable proposals
        """
        proposal_ids = self.hiring_box.keys()
        proposals = Proposal.objects.filter(id__in=proposal_ids)
        hiring_box = self.hiring_box.copy()

        for proposal in proposals:
            hiring_box[str(proposal.id)]["proposal"] = proposal

        for member in hiring_box.values():
            member["total_price"] = member["salary"] * member["member_qty"]
            yield member


    def __len__(self):
        """
        Get the hiring_box data and count the members
        """
        return len(self.hiring_box.values())


    def get_total_freelancer(self):
        return self.__len__()
        # return sum(member["member_qty"] for member in self.hiring_box.values())

    def get_total_price_before_fee_and_discount(self):
        self.subtotal = sum((member["salary"] * member["member_qty"]) for member in self.hiring_box.values())
        return self.subtotal
        # return sum((member["salary"]) * member["member_qty"] for member in self.hiring_box.values())

    def get_gateway(self):
        if settings.PROPOSALGATEWAY_SESSION_ID in self.session:
            return PaymentGateway.objects.get(id=self.session[settings.PROPOSALGATEWAY_SESSION_ID]["gateway_id"])
        return None

    def get_fee_payable(self):
        newprocessing_fee = 0
        if settings.PROPOSALGATEWAY_SESSION_ID in self.session:
            newprocessing_fee = self.get_gateway().processing_fee
        return newprocessing_fee

    def get_discount_multiplier(self):
        # subtotal = sum((member["salary"]) * member["member_qty"] for member in self.hiring_box.values())
        # subtotal = self.get_total_price_before_fee_and_discount()
        subtotal = self.subtotal
        rate = 0
        if (get_level_one_start_amount() <= subtotal <= get_level_one_delta_amount()):
            rate = get_level_one_rate()

        if (get_level_two_start_amount() <= subtotal <= get_level_two_delta_amount()):
            rate = get_level_two_rate()

        if (get_level_three_start_amount() <= subtotal <= get_level_three_delta_amount()):
            rate = get_level_three_rate()

        if subtotal > get_level_four_start_amount():
            rate = get_level_four_rate()
        return rate
        
    def get_discount_value(self):
        discount = 0
        # subtotal = sum((member["salary"]) * member["member_qty"] for member in self.hiring_box.values())
        subtotal = self.get_total_price_before_fee_and_discount()

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


    def get_total_price_after_discount_only(self):
        saving_in_discount = 0
        subtotal = self.get_total_price_before_fee_and_discount()

        if settings.PROPOSALGATEWAY_SESSION_ID in self.session:
            saving_in_discount = subtotal - self.get_discount_value()
        return saving_in_discount

    def get_total_price_after_discount_only(self):
        subtotal = sum((member["salary"] * member["member_qty"]) for member in self.hiring_box.values())
        subtotal = self.get_total_price_before_fee_and_discount()
        total_after_discount = (subtotal - self.get_discount_value())
        return total_after_discount

    def get_total_price_after_discount_and_fee(self):
        subtotal = sum((member["salary"] * member["member_qty"]) for member in self.hiring_box.values())
        processing_fee = self.get_fee_payable()
        grandtotal = ((subtotal - self.get_discount_value()) + processing_fee)
        return grandtotal

    def remove(self, proposal):
        """
        Delete item from hiring_box
        """
        proposal_id = str(proposal)
        if proposal_id in self.hiring_box:
            del self.hiring_box[proposal_id]
            self.commit()


    def commit(self):
        self.session.modified = True


    def clean_box(self):
        del self.session[settings.HIRINGBOX_SESSION_ID]
        del self.session[settings.PROPOSALGATEWAY_SESSION_ID]
        self.commit()


