from .models import Application
from general_settings.models import PaymentGateway
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
    get_level_four_start_amount
)


class ApplicationAddon():
    """
    This is the base class for Application addon sessions
    """

    def __init__(self, request):
        self.session = request.session
        applicant_box = self.session.get('application')
        if 'application' not in request.session:
            applicant_box = self.session['application'] = {}
        self.applicant_box = applicant_box

    def addon(self, application):
        """
        This function will add application to session
        This function will ONLY add applications with status "Accepted"
        """
        application_id = str(application.id)
        if application_id in self.applicant_box:
            self.applicant_box[application_id]["applicant"] = application
        else:
            self.applicant_box[application_id] = {'budget': int(application.budget)}
        self.commit()

    def __iter__(self):
        """
        Collect the application_ids in the session data to query the database
        and return applications
        """
        application_ids = self.applicant_box.keys()
        applications = Application.objects.filter(id__in=application_ids)
        applicant_box = self.applicant_box.copy()

        for application in applications:
            applicant_box[str(application.id)]["application"] = application

        for item in applicant_box.values():
            item["total_price"] = item["budget"]
            yield item

    def remove(self, application):
        """
        Delete item from applicant_box
        """
        application_id = str(application)
        if application_id in self.applicant_box:
            del self.applicant_box[application_id]
            self.commit()

    def __len__(self):
        return len(self.applicant_box.values())

    def get_total_applicants(self):
        return len(self.applicant_box.values())

    def get_total_price_before_fee_and_discount(self):
        return sum((application["budget"]) for application in self.applicant_box.values())

    def get_gateway(self):
        if "applicationgateway" in self.session:
            return PaymentGateway.objects.get(id=self.session["applicationgateway"]["gateway_id"])
        return None

    def get_fee_payable(self):
        newprocessing_fee = 0
        if "applicationgateway" in self.session:
            newprocessing_fee = self.get_gateway().processing_fee
        return newprocessing_fee

    def get_discount_value(self):
        discount = 0
        subtotal = sum((application["budget"]) for application in self.applicant_box.values())

        if (get_level_one_start_amount() <= subtotal <= get_level_one_delta_amount()):
            discount = 0

        if (get_level_two_start_amount() <= subtotal <= get_level_two_delta_amount()):
            discount = ((subtotal * get_level_two_rate())/100)

        if (get_level_three_start_amount() <= subtotal <= get_level_three_delta_amount()):
            discount = ((subtotal * get_level_three_rate())/100)

        if subtotal > get_level_four_start_amount():
            discount = ((subtotal * get_level_four_rate())/100)
            print(get_level_four_rate())

        total_discount = round(discount)
        print(total_discount)
        return total_discount


    def get_start_discount_value(self):
        return get_level_two_start_amount()

    def get_discount_multiplier(self):
        subtotal = sum((application["budget"]) for application in self.applicant_box.values())

        if (get_level_one_start_amount() <= subtotal <= get_level_one_delta_amount()):
            return get_level_one_rate()

        elif (get_level_two_start_amount() <= subtotal <= get_level_two_delta_amount()):
            return get_level_two_rate()

        elif (get_level_three_start_amount() <= subtotal <= get_level_three_delta_amount()):
            return get_level_three_rate()

        elif subtotal > get_level_four_start_amount():
            return get_level_four_rate()
        return 0

    def get_total_price_after_discount_only(self):
        saving_in_discount = 0
        subtotal = self.get_total_price_before_fee_and_discount()

        if "applicationgateway" in self.session:
            saving_in_discount = subtotal - self.get_discount_value()
        return saving_in_discount

    def get_total_price_after_discount_and_fee(self):
        subtotal = sum((application["budget"])
                       for application in self.applicant_box.values())
        processing_fee = 0

        if "applicationgateway" in self.session and subtotal > 0:
            processing_fee = PaymentGateway.objects.get(
                id=self.session["applicationgateway"]["gateway_id"]).processing_fee

        grandtotal = ((subtotal - self.get_discount_value()) + processing_fee)
        return grandtotal

    def commit(self):
        self.session.modified = True

    def clean_box(self):
        del self.session['application']
        del self.session['applicationgateway']
        self.commit()
