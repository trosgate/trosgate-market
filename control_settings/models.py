from django.db import models
from  embed_video.fields  import  EmbedVideoField
from general_settings . models import (
    PaymentGateway, PaymentAPIs, Payday,  DiscountSystem,
    TestEmail, SubscriptionGateway, HiringFee, ExachangeRateAPI,
    PaymentsControl, Mailer, DepositControl
)
from django.utils.translation import gettext_lazy as _


class PaydayController(Payday):
    class Meta:
        proxy=True
        verbose_name = _("Payday Control")
        verbose_name_plural = _("Payday Control")


class PaymentsController(PaymentsControl):
    class Meta:
        proxy=True
        verbose_name = _("Payments Control")
        verbose_name_plural = _("Payments Control")


class DepositController(DepositControl):
    class Meta:
        proxy=True
        verbose_name = _("Deposit Control")
        verbose_name_plural = _("Deposit Control")


class ExchangeRateSetting(ExachangeRateAPI):
    class Meta:
        proxy=True
        verbose_name = _("Currency Exchange Setting")
        verbose_name_plural = _("Currency Exchange Setting")


class GatewaySetting(PaymentGateway):
    class Meta:
        proxy=True
        ordering = ['ordering']
        verbose_name = _("Payment Gateway")
        verbose_name_plural = _("Payment Gateway")


class HiringSetting(HiringFee):
    class Meta:
        proxy=True
        verbose_name = _("Hiring Fee Setting")
        verbose_name_plural = _("Hiring Fee Setting")


class PaymentAPISetting(PaymentAPIs):
    class Meta:
        proxy=True
        verbose_name = _("Payment API")
        verbose_name_plural = _("Payment API")


class DiscountSettings(DiscountSystem):
    class Meta:
        proxy=True
        verbose_name = _("Discount System")
        verbose_name_plural = _("Discount System")


class MailerSetting(Mailer):
    class Meta:
        proxy=True
        verbose_name = _("Mailer")
        verbose_name_plural = _("Mailer")


class TestMailSetting(TestEmail):
    class Meta:
        proxy=True
        verbose_name = _("Test Email")
        verbose_name_plural = _("Test Email")


class SubscriptionSetting(SubscriptionGateway):
    class Meta:
        proxy=True
        verbose_name = _("Subscription Setting")
        verbose_name_plural = _("Subscription Setting")























































































