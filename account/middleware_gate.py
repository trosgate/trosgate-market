# middleware.py
import re
from django.conf import settings
from account.models import Merchant, Customer
from django.http import  HttpResponseRedirect
from django.urls import reverse
from threadlocals.threadlocals import set_thread_variable
from django.shortcuts import get_object_or_404


class MerchantGateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allow_list_patterns = [re.compile(fr"^{allowed}$") for allowed in settings.MERCHANT_GATE_ALLOW_LIST]

    def __call__(self, request):
        if request.user.is_authenticated and request.user.user_type != Customer.ADMIN:
            request.merchant = get_object_or_404(Merchant, pk=request.user.active_merchant_id)
            set_thread_variable('merchant_user', request.merchant.merchant)
            gate_url = reverse("merchants:subscription")

            if request.merchant and request.user.is_merchant:
                allowed_conditions = [
                    request.merchant.type in Merchant.ACTIVE_TYPES,
                    request.path_info == gate_url,
                    any(pattern.match(request.path_info) for pattern in self.allow_list_patterns)
                ]

                if any(allowed_conditions):
                    return self.get_response(request)

                return HttpResponseRedirect(gate_url)

        return self.get_response(request)
