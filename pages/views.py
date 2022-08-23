from django.shortcuts import render, redirect
from .models import TermsAndConditions, Hiring, Freelancing, Sponsorship
from .forms import SponsorForm
from django.contrib import messages
from general_settings.discount import (
    get_level_one_rate,
    get_level_two_rate, 
    get_level_three_rate, 
    get_level_four_rate,
    get_level_one_start_amount, 
    get_level_one_delta_amount, 
    get_level_two_start_amount, 
    get_level_two_delta_amount, 
    get_level_three_start_amount, 
    get_level_three_delta_amount, 
    get_level_four_start_amount,
    get_discount_calculator,
    get_earning_calculator
)
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from general_settings.fees_and_charges import (
    get_contract_fee_percentage,
    get_contract_fee_extra,
    get_contract_delta_amount,
    get_contract_fee_calculator, ###(amount)
    get_proposal_fee_percentage,
    get_proposal_fee_extra,
    get_proposal_delta_amount,
    get_proposal_fee_calculator, ###(amount)
    get_application_fee_percentage,
    get_application_fee_extra,
    get_application_delta_amount,
    get_application_fee_calculator, ###(amount)
    get_extra_application_value,
    get_extra_proposal_value,
    get_extra_contract_value   
)
from general_settings.models import PaymentGateway

def terms_and_conditions(request):
    termsandcond = TermsAndConditions.objects.filter(is_published = True)
    return render(request, "pages/terms_and_conditions.html", {"termsandcond":termsandcond})


def how_it_works(request):
    hiring = Hiring.objects.filter(is_published = True)
    freelancing = Freelancing.objects.filter(is_published = True)
    gateways = PaymentGateway.objects.filter(status=True)

    level_one_rate = get_level_one_rate() 
    level_one_start_amount = get_level_one_start_amount()
    level_one_delta_amount = get_level_one_delta_amount()
    level_two_rate = get_level_two_rate()
    level_two_start_amount = get_level_two_start_amount()
    level_two_delta_amount = get_level_two_delta_amount()
    level_three_rate = get_level_three_rate()
    level_three_start_amount = get_level_three_start_amount()
    level_three_delta_amount = get_level_three_delta_amount()
    level_four_rate = get_level_four_rate()
    level_four_start_amount = get_level_four_start_amount()
    # Discount Value
    l1_discount_amount = get_discount_calculator(level_one_delta_amount, level_one_delta_amount, level_one_rate)
    l2_discount_amount = get_discount_calculator(level_two_start_amount, level_two_start_amount, level_two_rate)
    l3_discount_amount = get_discount_calculator(level_three_start_amount, level_three_start_amount, level_three_rate)
    l4_discount_amount = get_discount_calculator(level_four_start_amount, level_four_start_amount, level_four_rate)
    # Gross Sales
    l1_disc_sales_price=level_one_delta_amount - l1_discount_amount
    l2_disc_sales_price=level_two_start_amount - l2_discount_amount
    l3_disc_sales_price=level_three_start_amount - l3_discount_amount
    l4_disc_sales_price=level_four_start_amount - l4_discount_amount

    # Extra Application Fee Value
    l1_extra_application_value = get_extra_application_value(l1_disc_sales_price)
    l2_extra_application_value = get_extra_application_value(l2_disc_sales_price)
    l3_extra_application_value = get_extra_application_value(l3_disc_sales_price)
    l4_extra_application_value = get_extra_application_value(l4_disc_sales_price)
    # Extra Proposal Fee Value
    l1_extra_proposal_value = get_extra_proposal_value(l1_disc_sales_price)
    l2_extra_proposal_value = get_extra_proposal_value(l2_disc_sales_price)
    l3_extra_proposal_value = get_extra_proposal_value(l3_disc_sales_price)
    l4_extra_proposal_value = get_extra_proposal_value(l4_disc_sales_price)
    # Extra Contract Fee Value
    l1_extra_contract_value = get_extra_contract_value(l1_disc_sales_price)
    l2_extra_contract_value = get_extra_contract_value(l2_disc_sales_price)
    l3_extra_contract_value = get_extra_contract_value(l3_disc_sales_price)
    l4_extra_contract_value = get_extra_contract_value(l4_disc_sales_price)

    l1_proposal_net_earning = round(l1_disc_sales_price - get_proposal_fee_calculator(l1_disc_sales_price))
    l2_proposal_net_earning = round(l2_disc_sales_price - get_proposal_fee_calculator(l2_disc_sales_price))
    l3_proposal_net_earning = round(l3_disc_sales_price - get_proposal_fee_calculator(l3_disc_sales_price))
    l4_proposal_net_earning = round(l4_disc_sales_price - get_proposal_fee_calculator(l4_disc_sales_price))
    
    l1_contract_net_earning = round(l1_disc_sales_price - get_contract_fee_calculator(l1_disc_sales_price))
    l2_contract_net_earning = round(l2_disc_sales_price - get_contract_fee_calculator(l2_disc_sales_price))
    l3_contract_net_earning = round(l3_disc_sales_price - get_contract_fee_calculator(l3_disc_sales_price))
    l4_contract_net_earning = round(l4_disc_sales_price - get_contract_fee_calculator(l4_disc_sales_price))
    
    l1_application_net_earning = round(l1_disc_sales_price - get_application_fee_calculator(l1_disc_sales_price))
    l2_application_net_earning = round(l2_disc_sales_price - get_application_fee_calculator(l2_disc_sales_price))
    l3_application_net_earning = round(l3_disc_sales_price - get_application_fee_calculator(l3_disc_sales_price))
    l4_application_net_earning = round(l4_disc_sales_price - get_application_fee_calculator(l4_disc_sales_price))

    context ={
        "hiring":hiring, 
        'freelancing':freelancing, 
        'gateways':gateways, 
        'l1_proposal_net_earning':l1_proposal_net_earning, 
        'l2_proposal_net_earning':l2_proposal_net_earning, 
        'l3_proposal_net_earning':l3_proposal_net_earning, 
        'l4_proposal_net_earning':l4_proposal_net_earning, 
        'l1_contract_net_earning':l1_contract_net_earning, 
        'l2_contract_net_earning':l2_contract_net_earning, 
        'l3_contract_net_earning':l3_contract_net_earning, 
        'l4_contract_net_earning':l4_contract_net_earning,
        'l1_application_net_earning':l1_application_net_earning, 
        'l2_application_net_earning':l2_application_net_earning, 
        'l3_application_net_earning':l3_application_net_earning, 
        'l4_application_net_earning':l4_application_net_earning,
        'l1_discount_amount':l1_discount_amount, 
        'l2_discount_amount':l2_discount_amount, 
        'l3_discount_amount':l3_discount_amount, 
        'l4_discount_amount':l4_discount_amount, 
        'l1_disc_sales_price':l1_disc_sales_price, 
        'l2_disc_sales_price':l2_disc_sales_price, 
        'l3_disc_sales_price':l3_disc_sales_price, 
        'l4_disc_sales_price':l4_disc_sales_price,
        'l1_extra_proposal_value':l1_extra_proposal_value, 
        'l2_extra_proposal_value':l2_extra_proposal_value, 
        'l3_extra_proposal_value':l3_extra_proposal_value, 
        'l4_extra_proposal_value':l4_extra_proposal_value, 
        'l1_extra_application_value':l1_extra_application_value, 
        'l2_extra_application_value':l2_extra_application_value, 
        'l3_extra_application_value':l3_extra_application_value, 
        'l4_extra_application_value':l4_extra_application_value, 
        'l1_extra_contract_value':l1_extra_contract_value, 
        'l2_extra_contract_value':l2_extra_contract_value, 
        'l3_extra_contract_value':l3_extra_contract_value, 
        'l4_extra_contract_value':l4_extra_contract_value, 
        'base_currency_symbol':get_base_currency_symbol(), 
        'level_one_rate':level_one_rate, 
        'level_one_start_amount':level_one_start_amount,
        'level_one_delta_amount':level_one_delta_amount,
        'level_two_rate':level_two_rate,
        'level_two_start_amount':level_two_start_amount,
        'level_two_delta_amount':level_two_delta_amount,
        'level_three_rate':level_three_rate,
        'level_three_start_amount':level_three_start_amount,
        'level_three_delta_amount':level_three_delta_amount,
        'level_four_rate':level_four_rate,
        'level_four_start_amount':level_four_start_amount,
        'contract_fee_percentage':get_contract_fee_percentage(),
        'contract_fee_extra':get_contract_fee_extra(),
        'contract_delta_amount':get_contract_delta_amount(),
        'proposal_fee_percentage':get_proposal_fee_percentage(),
        'proposal_fee_extra':get_proposal_fee_extra(),
        'proposal_delta_amount':get_proposal_delta_amount(),
        'application_fee_percentage':get_application_fee_percentage(),
        'application_fee_extra':get_application_fee_extra(),
        'application_delta_amount':get_application_delta_amount(),
    }
    return render(request, "pages/howitworks.html", context)