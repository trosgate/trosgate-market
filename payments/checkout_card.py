import re
from datetime import datetime
class CreditCard:
    CARD_TYPES = {
        'visa': '^4[0-9]{12}(?:[0-9]{3})?$',
        'mastercard': '^5[1-5][0-9]{14}$',
        'discover': '^6(?:011|5[0-9]{2})[0-9]{12}$',
        'amex': '^3[47][0-9]{13}$',
    }

    def __init__(self, number, exp_month, exp_year, cvc):
        self.number = number.replace(' ', '')
        self.exp_month = exp_month
        self.exp_year = exp_year
        self.cvc = cvc

    def validate(self):
        # Validate card number
        if not self._validate_number():
            return False

        # Validate expiration date
        if not self._validate_expiration():
            return False

        # Validate CVC
        if not self._validate_cvc():
            return False

        return True

    def _validate_number(self):
        # Check if the card number is valid
        if not re.match(r'^\d{13,19}$', self.number):
            return False

        # Check the card type
        for card_type, pattern in self.CARD_TYPES.items():
            if re.match(pattern, self.number):
                self.card_type = card_type
                return True

        return False

    def _validate_expiration(self):
        # Check if expiration date is in the future
        if self.exp_year < int(datetime.strftime('%Y')):
            return False
        if self.exp_year == int(datetime.strftime('%Y')) and self.exp_month < int(datetime.strftime('%m')):
            return False
        return True

    def _validate_cvc(self):
        # Check if the CVC is valid
        if not re.match(r'^\d{3,4}$', self.cvc):
            return False

        # Check the CVC length based on card type
        if self.card_type == 'amex' and len(self.cvc) != 4:
            return False
        elif len(self.cvc) != 3:
            return False

        return True
