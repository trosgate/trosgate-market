from django.utils import timezone
from dateutil.relativedelta import relativedelta

# Utility function for freelancer search
def one_month():
    return (timezone.now() - relativedelta(months = 1))

def two_months():
    return (timezone.now() - relativedelta(months = 2))

def three_months():
    return (timezone.now() - relativedelta(months = 3))

def four_months():
    return (timezone.now() - relativedelta(months = 4))

def five_months():
    return (timezone.now() - relativedelta(months = 5))

def six_months():
    return (timezone.now() - relativedelta(months = 6))

def one_year():
    return (timezone.now() - relativedelta(years = 1))

def two_years():
    return (timezone.now() - relativedelta(years = 2))

def three_years():
    return (timezone.now() - relativedelta(years = 3))

def four_years():
    return (timezone.now() - relativedelta(years = 4))

def five_years():
    return (timezone.now() - relativedelta(years = 5))





