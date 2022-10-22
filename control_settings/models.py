from django.db import models
from general_settings . models import (
    PaymentGateway, PaymentAPIs, Payday,  DiscountSystem,
    TestEmail, SubscriptionGateway, HiringFee, ExachangeRateAPI,
    PaymentsControl, Mailer, DepositControl, DepositGateway
)
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


def home_layout_path(instance, filename):
    return "layout/%s/%s" % (instance.title_block, filename)


class LayoutSetting(models.Model):
    title_block = models.CharField(_("Banner Title"), max_length=100, default="Hire Experts or Team")
    subtitle_block = models.CharField(_("Banner Subtitle"), max_length=150, default="Consectetur adipisicing elit sed dotem eiusmod tempor incuntes ut labore etdolore maigna aliqua enim.")
    video_title = models.CharField(_("Royal Video Title"), max_length=100, default="See For Yourself!", null=True, blank=True)
    video_description = models.CharField(_("Royal Video Description"), max_length=100, default="Hire Experts or Team", null=True, blank=True)
    banner_type = models.BooleanField(_("Banner Type"), choices=((False, 'Switch Hero Banner'), (True, 'Switch Royal Banner')), default=False)
    video_url = models.URLField(_("Royal embed Video"), help_text=_("Your can Paste your Youtube or Vimeo video url here to embed. Only secured url allowed"), null=True, blank=True)
    banner_image = models.ImageField(_("Hero Image"), help_text=_("image must be any of these: 'JPEG','JPG','PNG','PSD'"), null=True, blank=True, upload_to=home_layout_path, validators=[FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])])
    banner_color = models.CharField(_("Hero Background Color"), max_length=100, default="purple", help_text=_("Put your color here to decorate Hero Banner Background and buttons like signup and login. Example '3F0F8FF', or 'red' or 'blue' or 'purple' or any css color code. Warning!: Donnot add quotation marks around the color attributes"), null=True, blank=True)
    banner_button_one_color = models.CharField(_("Hero Button1 Color"), max_length=100, default="green", help_text=_("Put your bootstrap color here to decorate Hero Button 1. Example 'primary' or 'secondary' or 'light' or 'success' . Warning!: Exclude quotation marks when you input color attributes"), null=True, blank=True)
    banner_button_two_color = models.CharField(_("Hero Button2 Color"), max_length=100, default="light", help_text=_("Put your bootstrap color here to decorate Hero Button 2. Example 'primary' or 'secondary' or 'light' or 'success' . Warning!: Exclude quotation marks when you input color attributes"), null=True, blank=True)

    show_gateways = models.BooleanField(_("Display Gateway"), default=True)
    gateway_title = models.CharField(_("Gateway Title"), max_length=100, default="Collection and Payout Methods", null=True, blank=True)
    
    category_title = models.CharField(_("Div Two Category Title"), max_length=100, default="Explore Categories", null=True, blank=True)
    category_subtitle = models.CharField(_("Div Two Category Subitle"), max_length=100, default="Professional by categories", null=True, blank=True)
    
    proposal_title = models.CharField(_("Div Three Proposal Title"), max_length=100, default="Explore Proposals", null=True, blank=True)
    proposal_subtitle = models.CharField(_("Div Three Proposal Subitle"), max_length=100, default="Verified Proposals", null=True, blank=True)
    
    promo_title = models.CharField(_("Div Four Promo Title"), max_length=100, default="#1 Choice For Businesses", null=True, blank=True)
    promo_subtitle = models.CharField(_("Div Four Promo Subitle"), max_length=100, default="Business on the Go", null=True, blank=True)
    promo_description = models.TextField(
        _("Div Four Promo Decription"), max_length=300, default="The Example Marketplace", null=True, blank=True)
    promo_image = models.ImageField(_("Promo Image"), upload_to='promo/', default='freelancer/awards/banner.png', null=True, blank=True,)

    project_title = models.CharField(_("Div Five Project Title"), max_length=100, default="Published Jobs", null=True, blank=True)
    project_subtitle = models.CharField(_("Div Five Project Subitle"), max_length=100, default="Apply and get Hired", null=True, blank=True)
    
    footer_description = models.TextField(_("Footer Content"), max_length=250, default="Dotem eiusmod tempor incune utnaem labore etdolore maigna aliqua enim poskina ilukita ylokem lokateise ination voluptate velit esse cillum dolore eu fugiat nulla pariatur lokaim urianewce", null=True, blank=True)

    class Meta:
        verbose_name = _("Homepage Layout")
        verbose_name_plural = _("Homepage Layout")

    def __str__(self):
        return str(self.title_block)


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
        verbose_name = 'Mailer Settings'
        verbose_name_plural = 'Mailer Settings'


class TestMailSetting(TestEmail):
    class Meta:
        proxy=True
        verbose_name = _("Testing Email Settings")
        verbose_name_plural = _("Testing Email Settings")


class SubscriptionSetting(SubscriptionGateway):
    class Meta:
        proxy=True
        verbose_name = _("Subscription Setting")
        verbose_name_plural = _("Subscription Setting")

class DepositSetting(DepositGateway):
    class Meta:
        proxy=True
        verbose_name = _("Deposit Setting")
        verbose_name_plural = _("Deposit Setting")























































































