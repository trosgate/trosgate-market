from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import AdminCredit


# @receiver(post_save, sender=AdminCredit)
# def approve_memo_post_save(sender, instance, created, **kwargs):

#     AdminCredit.approve_credit_memo(pk=instance.id)