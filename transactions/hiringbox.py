from proposals.models import Proposal
from general_settings.models import PaymentGateway, DiscountSystem
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
        hiring_box = self.session.get('proposal_box')
        if 'proposal_box' not in request.session:
            hiring_box = self.session['proposal_box'] = {}
        self.hiring_box = hiring_box


    def addon(self, proposal, member_qty):
        """
        This function will add proposal to session at its original price
        This function will modify proposal by updating member quantity that client wishes to hire
        """
        proposal_id = str(proposal.id)
        if proposal_id in self.hiring_box:
            self.hiring_box[proposal_id]["member_qty"] = member_qty
        else:
            self.hiring_box[proposal_id] = {'salary': int(
                proposal.salary), 'member_qty': int(member_qty)}
        self.commit()


    def modify(self, proposal, member_qty):
        """
        We grab the proposal as a string, 
        then On condition that we have proposal in session at its original price,
        This function will modify proposal by updating members quantity that client wishes to hire
        """
        proposal_id = str(proposal)

        if proposal_id in self.hiring_box:
            self.hiring_box[proposal_id]["member_qty"] = member_qty
        else:
            self.hiring_box[proposal_id] = {"price": int(
                proposal.salary), "member_qty": int(member_qty)}
        self.commit()


    def __iter__(self):
        """
        Collect the proposal_id in the session data to query the database
        and return proposals
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
        return sum(member["member_qty"] for member in self.hiring_box.values())


    def get_total_freelancer(self):
        return sum(member["member_qty"] for member in self.hiring_box.values())


    def get_total_price_before_fee_and_discount(self):
        return sum((member["salary"]) * member["member_qty"] for member in self.hiring_box.values())


    def get_gateway(self):
        if "proposalgateway" in self.session:
            return PaymentGateway.objects.get(id=self.session["proposalgateway"]["gateway_id"])
        return None


    def get_fee_payable(self):
        newprocessing_fee = 0
        if "proposalgateway" in self.session:
            newprocessing_fee = self.get_gateway().processing_fee
        return newprocessing_fee


    def get_discount_multiplier(self):
        subtotal = sum((member["salary"]) * member["member_qty"] for member in self.hiring_box.values())

        if (get_level_one_start_amount() <= subtotal <= get_level_one_delta_amount()):
            return get_level_one_rate()

        elif (get_level_two_start_amount() <= subtotal <= get_level_two_delta_amount()):
            return get_level_two_rate()

        elif (get_level_three_start_amount() <= subtotal <= get_level_three_delta_amount()):
            return get_level_three_rate()

        elif subtotal > get_level_four_start_amount():
            return get_level_four_rate()
        return 0


    def get_discount_value(self):
        discount = 0
        subtotal = sum((member["salary"]) * member["member_qty"] for member in self.hiring_box.values())

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

        if "proposalgateway" in self.session:
            saving_in_discount = subtotal - self.get_discount_value()
        return saving_in_discount


    def get_total_price_after_discount_and_fee(self):
        subtotal = sum((member["salary"]) * member["member_qty"] for member in self.hiring_box.values())
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
        del self.session['proposal_box']
        del self.session['proposalgateway']
        self.commit()


