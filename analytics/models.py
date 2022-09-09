from django.db import models
from django.utils.translation import gettext_lazy as _
from projects.models import Project
from projects . models import Project
from account . models import Customer
from transactions.models import ApplicationSale, Purchase, ProposalSale, ContractSale, SubscriptionItem


class NewStats(models.Model):
    description = models.CharField( _("NewStats"), default="Statistics data on website visitors", max_length=100, null=True, blank=True)
    win = models.PositiveIntegerField(help_text=_("To track, resolve all the values to zero to start tracking visitors"))
    mac = models.PositiveIntegerField(help_text=_("To track, resolve all the values to zero to start tracking visitors"))
    iph = models.PositiveIntegerField(help_text=_("To track, resolve all the values to zero to start tracking visitors"))
    android = models.PositiveIntegerField(help_text=_("To track, resolve all the values to zero to start tracking visitors"))
    oth = models.PositiveIntegerField(help_text=_("To track, resolve all the values to zero to start tracking visitors"))


    class Meta:
        verbose_name = _("Site Visitor Statistics")
        verbose_name_plural = _("Site Visitor Statistics")

    def __str__(self):
        return self.description


class SuccessProposal(ProposalSale):
    class Meta:
        proxy=True
        ordering = ('-created_at',)
        verbose_name = _("Proposal Paid")
        verbose_name_plural = _("Proposal Paid")


class SuccessApplication(ApplicationSale):
    class Meta:
        proxy=True
        ordering = ('-created_at',)
        verbose_name = _("Project Applicant Paid")
        verbose_name_plural = _("Project Applicant Paid")


class SuccessInternalContract(ContractSale):
    class Meta:
        proxy=True
        ordering = ('-created_at',)
        verbose_name = _("Internal Contracts Paid")
        verbose_name_plural = _("Internal Contracts Paid")


class UserStatistics(Customer):
    class Meta:
        proxy=True
        ordering = ('date_joined',)
        verbose_name = _("User Statistics")
        verbose_name_plural = _("User Statistics")













