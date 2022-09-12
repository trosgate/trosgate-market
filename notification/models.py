from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

'''
soon to add choices like following
    SUBSCRIPTION = 'subscription'
    APPLICATION = 'application'
    MESSAGE = 'message' #can be contract message or chat
    CONTRACT = 'contract'
    PROPOSAL = 'proposal'
    PROJECT = 'project'
    QUIZ = 'quiz'
    TEAM = 'team'
    ORDER = 'order'

    CHOICES = (
        (SUBSCRIPTION, _("Subscription")),
        (APPLICATION, _("Application")),
        (MESSAGE, _("Message")),
        (CONTRACT, _("contract")),
        (PROPOSAL, _("proposal")),
        (PROJECT, _("project")),
        (QUIZ, _("quiz")),
        (TEAM, _("Team")),
        (ORDER, _("Order")),
    )
'''
class Notification(models.Model): #Will be changed to Announcement from Admin

    APPLICATION = 'application'
    MESSAGE = 'message'

    CHOICES = (
        (APPLICATION, _("Application")),
        (MESSAGE, _("Message")),
    )

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Sender"), related_name="sendernotifications", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Receiver"), related_name='receivernotifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_read = models.BooleanField(default=False)
    extra_id = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.sender.short_name