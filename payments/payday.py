from general_settings.models import Payday
from proposals.utilities import (
    one_day, 
    two_days, 
    three_days, 
    four_days, 
    five_days, 
    six_days, 
    one_week,
    two_weeks,
    three_weeks,
    one_month,
)

def get_payday():
    try:
        return Payday.objects.get(id=1).payday_converter 
    except:
        return 'three_days'


def get_payday_deadline():
    if get_payday() == "one_day":
        return one_day()
    if get_payday() == "two_days":
        return two_days()
    if get_payday() == "three_days":
        return three_days()
    if get_payday() == "four_days":
        return four_days()
    if get_payday() == "five_days":
        return five_days()
    if get_payday() == "six_days":
        return six_days()
    if get_payday() == "one_week":
        return one_week()
    if get_payday() == "two_weeks":
        return two_weeks()
    if get_payday() == "three_weeks":
        return three_weeks()
    if get_payday() == "one_month":
        return one_month()










