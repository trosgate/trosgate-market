import calendar
import re
from datetime import datetime


class CreditCard:
    CARD_TYPES = {
        'visa': '^4[0-9]{12}(?:[0-9]{3})?$',
        'mastercard': '^5[1-5][0-9]{14}$',
        'discover': '^6(?:011|5[0-9]{2})[0-9]{12}$',
        'amex': '^3[47][0-9]{13}$',
    }

    def __init__(self, first_name, last_name, number, month, year, cvv, package, amount): 
        self.first_name = first_name
        self.last_name = last_name
        self.number = number.replace(' ', '')
        self.month = int(month)
        self.year = int(year)
        self.cvv = cvv.replace(' ', '')
        self.package = package
        self.amount = int(amount)


    def is_valid(self):
        # Validate card number
        if not self._validate_number():
            return False

        # Validate expiration date
        if not self._validate_expiration():
            return False

        # Validate CVC
        if not self._validate_cvv():
            return False
        
        # Validate all input fields
        if not self._validate_fields():
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
        """Check whether the credit card is expired or not"""
        # Check if expiration date is in the future
        if self.year < int(datetime.now().strftime('%Y')):
            return False
        if self.month < int(datetime.now().strftime('%m')):
            return False
        if self.year == int(datetime.now().strftime('%Y')) and self.month < int(datetime.now().strftime('%m')):
            return False
        return True
    

    @property
    def expire_date(self):
        """Returns the expiry date of the card in MM-YYYY format"""
        return '%02d-%04d' % (self.month, self.year)


    def _validate_fields(self):
        """Validate that all the required attributes of card are given"""
        return (self.first_name 
                and self.last_name
                and self.month
                and self.year
                and self.number
                and self.cvv
                and self.package
                and self.amount)
        

    def _validate_cvv(self):
        # Check if the CVC is valid
        if not re.match(r'^\d{3,4}$', self.cvv):
            return False

        # Check the CVC length based on card type
        if self.card_type == 'amex' and len(self.cvv) != 4:
            return False
        elif len(self.cvv) != 3:
            return False

        return True

