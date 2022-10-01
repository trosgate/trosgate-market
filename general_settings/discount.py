from .models import DiscountSystem

#GET RATES FOR DISCOUNT
def get_level_one_rate():
    try:
        return DiscountSystem.objects.get(id=1).level_one_rate 
    except:
        return 0

def get_level_two_rate():
    try:
        return DiscountSystem.objects.get(id=1).level_two_rate 
    except:
        return 0

def get_level_three_rate():
    try:
        return DiscountSystem.objects.get(id=1).level_three_rate 
    except:
        return 0

def get_level_four_rate():
    try:
        return DiscountSystem.objects.get(id=1).level_four_rate 
    except:
        return 0

#GET AMOUNT FOR DISCOUNT LEVEL ONE
def get_level_one_start_amount():
    try:
        return DiscountSystem.objects.get(id=1).level_one_start_amount 
    except:
        return 0

def get_level_one_delta_amount():
    try:
        return DiscountSystem.objects.get(id=1).level_one_delta_amount 
    except:
        return 0

#GET AMOUNT FOR DISCOUNT LEVEL TWO
def get_level_two_start_amount():
    try:
        return DiscountSystem.objects.get(id=1).level_two_start_amount 
    except:
        return 0

def get_level_two_delta_amount():
    try:
        return DiscountSystem.objects.get(id=1).level_two_delta_amount 
    except:
        return 0

#GET AMOUNT FOR DISCOUNT LEVEL THREE
def get_level_three_start_amount():
    try:
        return DiscountSystem.objects.get(id=1).level_three_start_amount 
    except:
        return 0

def get_level_three_delta_amount():
    try:
        return DiscountSystem.objects.get(id=1).level_three_delta_amount 
    except:
        return 0

#GET AMOUNT FOR DISCOUNT LEVEL FOUR
def get_level_four_start_amount():
    try:
        return DiscountSystem.objects.get(id=1).level_four_start_amount 
    except:
        return 0


def get_discount_value(amount, rate):
    return round(amount * (rate/100))


def get_discount_calculator(price_before_discount, total_before_discount, discount):
    return round(price_before_discount/total_before_discount * discount)

def get_earning_calculator(price_after_discount, fee):
    return round(price_after_discount - fee)

























