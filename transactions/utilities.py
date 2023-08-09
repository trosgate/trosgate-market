from transactions.models import Purchase, ProposalSale
from general_settings.fees_and_charges import get_proposal_fee_calculator
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from general_settings.discount import get_discount_calculator, get_earning_calculator


def calculate_payment_data(hiringbox):
    discount_value = hiringbox.get_discount_value()
    total_gateway_fee = hiringbox.get_fee_payable()
    grand_total_before_expense = hiringbox.get_total_price_before_fee_and_discount()
    grand_total = hiringbox.get_total_price_after_discount_and_fee()
    gateway_type = str(hiringbox.get_gateway())
    
    return {
        'discount_value': discount_value,
        'total_gateway_fee': total_gateway_fee,
        'grand_total_before_expense': grand_total_before_expense,
        'grand_total': grand_total,
        'gateway_type': gateway_type,
    }


class PurchaseAndSaleCreator:
    def create_purchase_and_sales(self, client, gateway_type, total_gateway_fee, grand_total, category, hiringbox, grand_total_before_expense, discount_value, stripe_order_key='', paypal_order_key='', razorpay_order_key=''):
        try:
            purchase = self._create_purchase(client, gateway_type, total_gateway_fee, grand_total, category, stripe_order_key, paypal_order_key,razorpay_order_key)
            self._create_proposal_sales(purchase, hiringbox, grand_total_before_expense, discount_value)
            return purchase
        except Exception as e:
            print('%s' % (str(e)))

    def _create_purchase(self, client, gateway_type, total_gateway_fee, grand_total, category, stripe_order_key='', paypal_order_key='', razorpay_order_key=''):
        return Purchase.objects.create(
            client=client,
            payment_method=str(gateway_type),
            client_fee=total_gateway_fee,
            category=category,
            salary_paid=grand_total,
            status=Purchase.FAILED,
            stripe_order_key=stripe_order_key,
            paypal_order_key=paypal_order_key,
            razorpay_order_key=razorpay_order_key
        )

    def _create_proposal_sales(self, purchase, hiringbox, grand_total_before_expense, discount_value):
        for proposal in hiringbox:
            ProposalSale.objects.create(
                package_name = proposal['package_name'],
                team=proposal["proposal"].team, 
                purchase=purchase,
                proposal=proposal["proposal"], 
                sales_price=int(proposal["salary"]), 
                staff_hired=proposal["member_qty"],
                earning_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),                   
                total_earning_fee_charged=round(get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),                   
                discount_offered=get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value),
                total_discount_offered=((get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                disc_sales_price=int(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)),
                total_sales_price=int((proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)) * proposal["member_qty"]),
                earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))), 
                total_earning=int(get_earning_calculator(
                    (proposal["salary"] - (get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value))),
                    get_proposal_fee_calculator(proposal["salary"] - get_discount_calculator(proposal["salary"], grand_total_before_expense, discount_value)))* proposal["member_qty"]) 
            )
