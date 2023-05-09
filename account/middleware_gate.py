# middleware.py
import re
from django.conf import settings
from account.models import Merchant
from django.http import  HttpResponseRedirect
from django.urls import reverse


class MerchantGateMiddleware:
    """
    Check that an account is in a valid status to permit access.
    Inactive accounts will be redirected to a plan selection page
    unless the URL is on an allowed list of routes.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.allow_list_patterns = [
            re.compile(fr"^{allowed}$") for allowed in settings.MERCHANT_GATE_ALLOW_LIST
        ]

    def __call__(self, request):
        
        if request.user.is_authenticated and request.user.is_merchant:

            # This attribute was set by upper lever middleware
            request.merchant = Merchant.objects.filter(pk=request.user.active_merchant_id).first()
            
            gate_url = reverse("merchants:subscription")
            if (
                request.merchant.type in Merchant.ACTIVE_TYPES
                or request.path_info == gate_url # MEANING THEY ARE WHERE THEY SHOULD BE CHECKING OUT
                or self.is_granted_passage(request.path_info)
            ):
                return self.get_response(request)

            return HttpResponseRedirect(gate_url)
        return self.get_response(request)

    def is_granted_passage(self, path):
        """Check if the request is allowed against the allow list."""
        return any(pattern.match(path) for pattern in self.allow_list_patterns)
