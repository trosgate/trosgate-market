from general_settings.models import SubscriptionGateway, DepositGateway


def subscription_switch():
    if SubscriptionGateway.objects.filter(pk=1).exists():
        subscript_switcher = SubscriptionGateway.objects.get(pk=1)
        return subscript_switcher

    else:
        subscript_switcher = SubscriptionGateway(pk=1, paypal=True, stripe=True, razorpay=True, flutterwave=True).save()
        return subscript_switcher


def deposit_switch():
    if DepositGateway.objects.filter(pk=1).exists():
        depo_switcher = DepositGateway.objects.get(pk=1)
        return depo_switcher

    else:
        depo_switcher = DepositGateway(pk=1, paypal=True, stripe=True, razorpay=True, flutterwave=True).save()
        return depo_switcher
