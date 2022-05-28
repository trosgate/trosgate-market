import requests
from .models import Currency, ExachangeRateAPI

#GET RATES FOR DISCOUNT
def get_base_currency_code():
    try:
        return Currency.objects.get(supported=True, default=True).code 
    except:
        return 'USD'

def get_base_currency_symbol():
    try:
        return Currency.objects.get(supported=True, default=True).symbol 
    except:
        return 'US$'

def get_exchange_rates_key():
    try:
        return ExachangeRateAPI.objects.get(id=1).exchange_rates_api_key 
    except:
        return ''


class CurrencyCalculator:
    def get_exchange_rates_path(self, from_currency_code):
        url_path = 'https://v6.exchangerate-api.com/v6/%s/latest/%s'
        url = url_path % (get_exchange_rates_key(), from_currency_code)
        r = requests.get(url)
        print('status:', r.status_code)
        if r.status_code == 200:
            return r.json()
        return ''

    def get_conversion_rate(self, from_currency_code, to_currency):
        return self.get_exchange_rates_path(from_currency_code)['conversion_rates'][to_currency]
      
    def get_converted_amount(self, from_currency_code, to_currency, target_amount):
        converted_amount = round((target_amount) * (self.get_conversion_rate(from_currency_code.upper(), to_currency.upper())), 2)
        return converted_amount
      
