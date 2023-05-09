from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models
from django.db.models import Aggregate
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from uuid import uuid4
from teams.utilities import create_random_code
from datetime import datetime, timezone, timedelta
from contract.models import InternalContract
from django.urls import reverse
from django.utils.text import slugify
from merchants.models import MerchantProduct, MerchantMaster


def proposal_images_path(instance, filename):
    return "proposal/%s/%s" % (instance.team.title, filename)


class ActiveProposals(models.Manager):
    def active_proposal(self):
        return super(ActiveProposals, self).get_queryset().filter(status=Proposal.ACTIVE)


class Proposal(MerchantProduct):
    revision = models.BooleanField(_("Revision"), choices=((False, 'No'), (True, 'Yes')), default=False)
    thumbnail = models.ImageField(_("Thumbnail"), help_text=_("image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312"), upload_to=proposal_images_path, validators=[FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])])
    team = models.ForeignKey('teams.Team', verbose_name=_("Team"), related_name="proposalteam", on_delete=models.CASCADE, max_length=250)
    faq_one = models.CharField(_("FAQ #1"), max_length=100)
    faq_one_description = models.TextField(_("FAQ #1 Details"), max_length=255)
    faq_two = models.CharField(_("FAQ #2"), max_length=100, null=True, blank=True)
    faq_two_description = models.TextField(_("FAQ #2 Details"), max_length=255, null=True, blank=True)
    faq_three = models.CharField(_("FAQ #3"), max_length=100, null=True, blank=True)
    faq_three_description = models.TextField(_("FAQ #3 Details"), max_length=255, null=True, blank=True)
 
    active = ActiveProposals()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Proposal")
        verbose_name_plural = _("Proposals")

    def __str__(self):
        return f'{self.title} - (Amount={self.salary}, Duration={self.get_dura_converter_display()})'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.thumbnail))

    image_tag.short_description = 'thumbnail'

    # absolute url for tender detail page
    def proposal_absolute_url(self):
        return reverse('proposals:proposal_preview', kwargs={'short_name': self.created_by.short_name, 'proposal_slug':self.slug})

    def tracking_time(self):
        return sum(tracker.minutes for tracker in self.trackings.all())

    def save(self, *args, **kwargs):
        if self.reference is None:
            try:
                self.reference = 'P' + str(uuid4()).split('-')[4]
            except:
                self.reference = 'P' + str(uuid4()).split('-')[4]
            self.slug=(slugify(self.title))
        super(Proposal, self).save(*args, **kwargs)


    @property
    def preview_proposal_sales_count(self):
        return self.proposalhired.filter(purchase__status='success').count()
    
    @property
    def preview_oneclick_sales_count(self):
        return self.oneclickproposal.filter(status='success').count()
    
    @property
    def preview_contract_sales_count(self):
        new_contract = 0
        contracts = InternalContract.objects.filter(proposal__id=self.id)
        for contract in contracts:
            new_contract = contract.contracthired.filter(purchase__status='success').count()
        return new_contract

    @property
    def aggregated_sales_count(self):
        return (self.preview_proposal_sales_count + self.preview_oneclick_sales_count + self.preview_contract_sales_count)


class ProposalSupport(Proposal):
    class Meta:
        proxy=True
        ordering = ['created_at']
        verbose_name = _("Proposal Support")
        verbose_name_plural = _("Proposal Support")


class ProposalChat(MerchantMaster):
    team = models.ForeignKey('teams.Team', verbose_name=_("Proposal Team"), related_name='proposalchats', on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, verbose_name=_("Proposal"), related_name='proposalschats', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Sender"), related_name='proposalsender', on_delete=models.CASCADE)
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_on']

    def __str__(self):
        return f'Message sent by {self.sender.get_full_name()}'






















