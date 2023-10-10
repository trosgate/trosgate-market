def get_base_currency(request):
    base_currency = request.merchant.merchant.country.currency.upper()
    return base_currency if base_currency else 'usd'


def calculate_payment_data(hiringbox):
    # This data apply to proposal,and project application
    discount_value = hiringbox.get_discount_value()
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    gateway_type = str(hiringbox.get_gateway())
    total_gateway_fee = hiringbox.get_fee_payable()
    
    return {
        'discount_value': discount_value,
        'total_gateway_fee': total_gateway_fee,
        'grand_total_before_expense': grand_total_before_expense,
        'grand_total': grand_total,
        'gateway_type': gateway_type,
    }


def calculate_contract_payment_data(hiringbox,contract):
    # This data apply to contract
    discount_value = hiringbox.get_discount_value(contract)
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount(contract)
    grand_total = hiringbox.get_total_price_after_discount_and_fee(contract)
    gateway_type = str(hiringbox.get_gateway())
    total_gateway_fee = hiringbox.get_fee_payable()
    
    return {
        'discount_value': discount_value,
        'total_gateway_fee': total_gateway_fee,
        'grand_total_before_expense': grand_total_before_expense,
        'grand_total': grand_total,
        'gateway_type': gateway_type,
    }





