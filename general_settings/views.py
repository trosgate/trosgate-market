from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .models import Category, WebsiteSetting, CurrencyConverter, Currency
from proposals.models import Proposal
from django.http import JsonResponse
from general_settings.currency import CurrencyCalculator, get_base_currency_code, get_exchange_rates_key 
from account.permission import user_is_client



def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, visible=True)
    proposals = category.proposal.filter(status = Proposal.ACTIVE)  
    # proposals = Proposal.objects.filter(category=category, status = Proposal.ACTIVE)
    print(proposals)
    context = {
        "category": category,
        'proposals':proposals,
    }
    return render(request, 'general_settings/category.html', context)


@login_required
@user_is_client
def currency_conversion(request):
    result = ''
    converted_amt = ''
    rate = ''
    message = ''
    exchange = ''
    checker = ''
    if request.POST.get('action') == 'currency':
        currency_id = int(request.POST.get('currencyid'))
        target_amount = int(request.POST.get('targetamount'))
        matching_qs = Currency.objects.get(id=currency_id, supported=True)
        converted_code = matching_qs.code
        exchange = CurrencyCalculator()

        try:
            result = exchange.get_exchange_rates_path(get_base_currency_code())
            converted_amt = exchange.get_converted_amount(get_base_currency_code(), matching_qs.code, target_amount)
            rate = exchange.get_conversion_rate(get_base_currency_code(), matching_qs.code)
            message = f'Amount {get_base_currency_code()}{target_amount} @ {rate} is = {converted_code}{converted_amt}'
        except:
            message = ('<span id="feedback-converter" style="color:red; text-align:right;">Ooops! The exchange API is down at the moment. Try again much later</span>')
        
        context = {
            'result': result,
            'message': message,
            'rate': rate,
            'checker': checker,

        }
        response = JsonResponse(context)
        return response

