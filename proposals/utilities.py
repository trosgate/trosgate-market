from datetime import datetime, timezone, timedelta
from django.utils.translation import gettext_lazy as _


# Duration conversion parameters for the proposal
def one_day():
    return (datetime.now() + timedelta(days = 1))

def two_days():
    return (datetime.now() + timedelta(days = 2))

def three_days():
    return (datetime.now() + timedelta(days = 3))

def four_days():
    return (datetime.now() + timedelta(days = 4))

def five_days():
    return (datetime.now() + timedelta(days = 5))

def six_days():
    return (datetime.now() + timedelta(days = 6))

def one_week():
    return (datetime.now() + timedelta(days = 7))

def two_weeks():
    return (datetime.now() + timedelta(days = 14))

def three_weeks():
    return (datetime.now() + timedelta(days = 21))

def one_month():
    return (datetime.now() + timedelta(days = 30))

def two_months():
    return (datetime.now() + timedelta(days = 60))

def three_months():
    return (datetime.now() + timedelta(days = 90))

def four_months():
    return (datetime.now() + timedelta(days = 120))

def five_months():
    return (datetime.now() + timedelta(days = 150))

def six_months():
    return (datetime.now() + timedelta(days = 180))



# def duration_converter(duration):
#     if duration == one_day():
#         return "01 Day"
#     elif duration == two_days():
#         return "02 Days"
#     elif duration == three_days():
#         return "03 Days"
#     elif duration == four_days():
#         return "04 Days"
#     elif duration == five_days():
#         return "05 Days"
#     elif duration == six_days():
#         return "06 Days"
#     elif duration == one_week():
#         return "01 Week"
#     elif duration == two_weeks():
#         return "02 Weeks"
#     elif duration == three_weeks():
#         return "03 Weeks"
#     elif duration == one_month():
#         return "01 Month"
#     elif duration == two_months():
#         return "02 Months"
#     elif duration == three_months():
#         return "03 Months"
#     elif duration == four_months():
#         return "04 Months"
#     elif duration == five_months():
#         return "05 Months"
#     elif duration == six_months():
#         return "06 Months"

