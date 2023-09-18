from account.models import Merchant
from django.contrib.sites.models import Site
from threadlocals.threadlocals import get_thread_variable


#GET RATES FOR DISCOUNT
def get_merchant_site():
    current_site = get_thread_variable('current_site')
    merchant =  current_site.merchant

    return merchant


def get_level_one_rate():
    level1_rate = get_merchant_site().level_one_rate if get_merchant_site() is not None else 0
    return level1_rate


def get_level_two_rate():
    level2_rate = get_merchant_site().level_two_rate if get_merchant_site() is not None else 0
    return level2_rate
    

def get_level_three_rate():
    level3_rate = get_merchant_site().level_three_rate if get_merchant_site() is not None else 0
    return level3_rate
    

def get_level_four_rate():
    level4_rate = get_merchant_site().level_four_rate if get_merchant_site() is not None else 0
    return level4_rate
    

#GET AMOUNT FOR DISCOUNT LEVEL ONE
def get_level_one_start_amount():
    level1_start_amount = get_merchant_site().level_one_start_amount if get_merchant_site() is not None else 0
    return level1_start_amount
    

def get_level_one_delta_amount():
    level1_delta_amount = get_merchant_site().level_one_delta_amount if get_merchant_site() is not None else 0
    return level1_delta_amount


#GET AMOUNT FOR DISCOUNT LEVEL TWO
def get_level_two_start_amount():
    level2_start_amount = get_merchant_site().level_two_start_amount if get_merchant_site() is not None else 0
    return level2_start_amount


def get_level_two_delta_amount():
    level2_delta_amount = get_merchant_site().level_two_delta_amount if get_merchant_site() is not None else 0
    return level2_delta_amount


#GET AMOUNT FOR DISCOUNT LEVEL THREE
def get_level_three_start_amount():
    level3_start_amount = get_merchant_site().level_three_start_amount if get_merchant_site() is not None else 0
    return level3_start_amount
    

def get_level_three_delta_amount():
    level3_delta_amount = get_merchant_site().level_three_delta_amount if get_merchant_site() is not None else 0
    return level3_delta_amount


#GET AMOUNT FOR DISCOUNT LEVEL FOUR
def get_level_four_start_amount():
    level4_start_amount = get_merchant_site().level_four_start_amount if get_merchant_site() is not None else 0
    return level4_start_amount


#determine the discount from value
def get_discount_value(amount, rate):
    return (amount * (rate/100))

def get_discount_calculator(price_before_discount, total_before_discount, discount):
    return (price_before_discount/total_before_discount * discount)

def get_earning_calculator(price_after_discount, fee):
    return (price_after_discount - fee)

























