from django.shortcuts import render, redirect
from .models import TermsAndConditions, Hiring, Freelancing, AboutUsPage, Investor
from django.contrib import messages
from django.http import JsonResponse
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
    get_discount_value
)
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from general_settings.fees_and_charges import (
    get_contract_fee_percentage,
    get_contract_fee_extra,
    get_contract_delta_amount,
    get_contract_fee_calculator,
    get_proposal_fee_percentage,
    get_proposal_fee_extra,
    get_proposal_delta_amount,
    get_proposal_fee_calculator,
    get_application_fee_percentage,
    get_application_fee_extra,
    get_application_delta_amount,
    get_application_fee_calculator,
    get_extra_application_value,
    get_extra_proposal_value,
    get_extra_contract_value   
)
from payments.models import PaymentGateway
from general_settings.models import Payday
from teams.models import Package
from control_settings.utilities import homepage_layout
from analytics.analytic import (
    total_freelancers,
    total_clients,
    total_teams,
    total_projects,
    total_projects_reopen,
    total_project_hired,
    total_proposals,
    total_proposal_hired,
    total_proposal_review_rate,
    total_internal_contracts,
    total_external_contracts,
    total_contracts_hired
)

from contract.models import InternalContract, Contract
from .forms import InvestorForm

def aboutus(request):
    # aboutpage=None
    # if AboutUsPage.objects.filter(pk=1).exists():
    aboutpage = AboutUsPage.objects.all().first()

    investor_form = InvestorForm()
    context={
        "aboutpage":aboutpage,
        "investor_form":investor_form,
        "home_layout":homepage_layout(),
        "freelancers":total_freelancers(),
        "clients":total_clients(),
        "teams":total_teams(),
        "proposals":total_proposals(),
        "proposal_hired_count":total_proposal_hired(),
        "proposal_review_rate":total_proposal_review_rate(),
        "projects":total_projects(),
        "projects_reopen":total_projects_reopen(),
        "total_hired":total_project_hired(),
        "internal_contracts":total_internal_contracts,
        "external_contracts":total_external_contracts,
        "contracts_paid":total_contracts_hired,
    }
    return render(request, "pages/aboutus.html", context)

def terms_and_conditions(request):
    termsandcond = TermsAndConditions.objects.filter(is_published = True)
    context={
        "home_layout":homepage_layout(),
        "termsandcond":termsandcond
    }
    return render(request, "pages/terms_and_conditions.html", context)


def how_it_works(request):
    
    hiring = Hiring.objects.filter(is_published = True)
    freelancing = Freelancing.objects.filter(is_published = True)
    gateways = PaymentGateway.objects.filter(status=True)
    packages = Package.objects.all()

    try:
        payday = Payday.objects.get(pk=1)
    except:
        payday = None
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
    l1_discount_amount = get_discount_value(level_one_delta_amount, level_one_rate)
    l2_discount_amount = get_discount_value(level_two_start_amount, level_two_rate)
    l3_discount_amount = get_discount_value(level_three_start_amount, level_three_rate)
    l4_discount_amount = get_discount_value(level_four_start_amount, level_four_rate)
    
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
        "home_layout":homepage_layout(), 
        "hiring":hiring, 
        'freelancing':freelancing, 
        'gateways':gateways, 
        'packages':packages, 
        'payday':payday, 
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


def start_investment_now(request):
    successful = ''
    if request.POST.get('action') == 'invest-now':
        salutation = request.POST.get('invSalute')
        name = request.POST.get('invName')
        email = request.POST.get('invEmail')
        confirm_email = request.POST.get('invConfirmEmail')
        if email == confirm_email:
            try:
                Investor.check_or_create(
                    salutation=salutation,
                    myname=name,
                    myemail=email, 
                    myconfirm_email=confirm_email
                )
                successful = "Information Saved. We shall keep in touch"
            except Exception as e:
                successful = str(e)
                print(successful)
            return JsonResponse({'success':successful})
        return JsonResponse({'success':"Sorry! Emails donnot match"})













