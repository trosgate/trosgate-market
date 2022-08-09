from datetime import timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta



# Duration conversion parameters for the proposal, projects and contracts
def one_day():
    return (timezone.now() + timedelta(days = 1))

def two_days():
    return (timezone.now() + timedelta(days = 2))

def three_days():
    return (timezone.now() + timedelta(days = 3))

def four_days():
    return (timezone.now() + timedelta(days = 4))

def five_days():
    return (timezone.now() + timedelta(days = 5))

def six_days():
    return (timezone.now() + timedelta(days = 6))

def one_week():
    return (timezone.now() + timedelta(weeks = 1))

def two_weeks():
    return (timezone.now() + timedelta(weeks = 2))

def three_weeks():
    return (timezone.now() + timedelta(weeks = 3))

def one_month():
    return (timezone.now() + relativedelta(months = 1))

def two_months():
    return (timezone.now() + relativedelta(months = 2))

def three_months():
    return (timezone.now() + relativedelta(months = 3))

def four_months():
    return (timezone.now() + relativedelta(months = 4))

def five_months():
    return (timezone.now() + relativedelta(months = 5))

def six_months():
    return (timezone.now() + relativedelta(months = 6))


#prev function with datetime

# def three_months():
#     return (timezone.now() + timedelta(days = 90))

# def four_months():
#     return (timezone.now() + timedelta(days = 120))

# def five_months():
#     return (timezone.now() + timedelta(days = 150))
