from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import HelpDesk, Ticket, TicketMessage
from django.utils.translation import gettext_lazy as _
from notification.mailer import ticket_reply_email


@receiver(post_save, sender=HelpDesk)
def help_desk_default_setting(sender, instance, created, **kwargs):
    '''
    This function ensures that, at any given time, 
    one instance of help desk will be published so far as it exists
    '''
    HelpDesk.objects.filter(published=True).update(published=False)
    HelpDesk.objects.filter(pk=instance.id).update(published=True)


@receiver(post_save, sender=TicketMessage)
def ticket_message_support(sender, instance, created, **kwargs):
    if created and instance.action == True: # If action is True, it means action came from Admin User
        ticket = instance
        ticket.support=instance.ticket.support
        ticket.save()

        try:
            ticket_reply_email(instance)
        except Exception as e:
            print('%s' % (str(e)))
            

