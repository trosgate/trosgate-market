from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from teams.utilities import create_random_code
from merchants.models import MerchantMaster


class Message(MerchantMaster):
    sender = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Receiver"), blank=True, null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.sender
    

class Room(MerchantMaster):
    WAITING = 'waiting'
    ACTIVE = 'active'
    CLOSED = 'closed'
    CHOICES = (
        (WAITING, _("Waiting")),
        (ACTIVE, _("Active")),
        (CLOSED, _("Closed")),
    )

    reference = models.CharField(max_length=255)
    guest = models.CharField(max_length=255)
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Agent"), related_name="rooms", blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=CHOICES, default=WAITING)
    messages = models.ManyToManyField(Message, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    page_name = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.agent)
    
    # def save(self, *args, **kwargs):
    #     if self.reference is None or self.reference == "":
    #         self.reference = create_random_code()            
    #     super(Room, self).save(*args, **kwargs)