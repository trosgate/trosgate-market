from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProjectResolution, ProposalResolution
from proposals.utilities import (
    one_day, two_days, three_days, four_days, 
    five_days, six_days, one_week, two_weeks,
    three_weeks, one_month,
    #Below additional times apply to contract
    two_months, three_months, four_months, five_months, six_months
)


@receiver(post_save, sender=ProjectResolution)
def create_endtime_of_project(sender, instance, created, **kwargs):

    if created and instance.application.project.completion_time == instance.ONE_DAY:
        ProjectResolution.objects.filter(pk=instance.id).update(end_time = one_day())
    if created and instance.application.project.completion_time == instance.TWO_DAYS:
        ProjectResolution.objects.filter(pk=instance.id).update(end_time = two_days())
    if created and instance.application.project.completion_time == instance.THREE_DAYS:
        ProjectResolution.objects.filter(pk=instance.id).update(end_time = three_days())
    if created and instance.application.project.completion_time == instance.FOUR_DAYS:
        ProjectResolution.objects.filter(pk=instance.id).update(end_time = four_days())
    if created and instance.application.project.completion_time == instance.FIVE_DAYS:
        ProjectResolution.objects.filter(pk=instance.id).update(end_time = five_days())
    if created and instance.application.project.completion_time == instance.SIX_DAYS:
        ProjectResolution.objects.filter(pk=instance.id).update(end_time = six_days())
    if created and instance.application.project.completion_time == instance.ONE_WEEK:
        ProjectResolution.objects.filter(pk=instance.id).update(end_time = one_week())
    if created and instance.application.project.completion_time == instance.TWO_WEEK:
        ProjectResolution.objects.filter(pk=instance.id).update(end_time = two_weeks())
    if created and instance.application.project.completion_time == instance.THREE_WEEK:
        ProjectResolution.objects.filter(pk=instance.id).update(end_time = three_weeks())
    if created and instance.application.project.completion_time == instance.ONE_MONTH:
        ProjectResolution.objects.filter(pk=instance.id).update(end_time = one_month())


@receiver(post_save, sender=ProposalResolution)
def create_endtime_of_proposal(sender, instance, created, **kwargs):
    if created and instance.proposal_sale.proposal.dura_converter == instance.ONE_DAY:
        ProposalResolution.objects.filter(pk=instance.id).update(end_time = one_day())
    if created and instance.proposal_sale.proposal.dura_converter == instance.TWO_DAYS:
        ProposalResolution.objects.filter(pk=instance.id).update(end_time = two_days())
    if created and instance.proposal_sale.proposal.dura_converter == instance.THREE_DAYS:
        ProposalResolution.objects.filter(pk=instance.id).update(end_time = three_days())
    if created and instance.proposal_sale.proposal.dura_converter == instance.FOUR_DAYS:
        ProposalResolution.objects.filter(pk=instance.id).update(end_time = four_days())
    if created and instance.proposal_sale.proposal.dura_converter == instance.FIVE_DAYS:
        ProposalResolution.objects.filter(pk=instance.id).update(end_time = five_days())
    if created and instance.proposal_sale.proposal.dura_converter == instance.SIX_DAYS:
        ProposalResolution.objects.filter(pk=instance.id).update(end_time = six_days())
    if created and instance.proposal_sale.proposal.dura_converter == instance.ONE_WEEK:
        ProposalResolution.objects.filter(pk=instance.id).update(end_time = one_week())
    if created and instance.proposal_sale.proposal.dura_converter == instance.TWO_WEEK:
        ProposalResolution.objects.filter(pk=instance.id).update(end_time = two_weeks())
    if created and instance.proposal_sale.proposal.dura_converter == instance.THREE_WEEK:
        ProposalResolution.objects.filter(pk=instance.id).update(end_time = three_weeks())
    if created and instance.proposal_sale.proposal.dura_converter == instance.ONE_MONTH:
        ProposalResolution.objects.filter(pk=instance.id).update(end_time = one_month())







