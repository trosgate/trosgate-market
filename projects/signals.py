from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project

from proposals.utilities import (
    one_day, two_days, three_days, four_days, 
    five_days, six_days, one_week, two_weeks,
    three_weeks, one_month,
)


# @receiver(post_save, sender=Project)
# def create_deadline_of_project(sender, instance, created, **kwargs):
#     if created and instance.dura_converter == "one_day":
#         Project.objects.filter(pk=instance.id).update(duration = one_day())
#     if created and instance.dura_converter == "two_days":
#         Project.objects.filter(pk=instance.id).update(duration = two_days())
#     if created and instance.dura_converter == "three_days":
#         Project.objects.filter(pk=instance.id).update(duration = three_days())
#     if created and instance.dura_converter == "four_days":
#         Project.objects.filter(pk=instance.id).update(duration = four_days())
#     if created and instance.dura_converter == "five_days":
#         Project.objects.filter(pk=instance.id).update(duration = five_days())
#     if created and instance.dura_converter == "six_days":
#         Project.objects.filter(pk=instance.id).update(duration = six_days())
#     if created and instance.dura_converter == "one_week":
#         Project.objects.filter(pk=instance.id).update(duration = one_week())
#     if created and instance.dura_converter == "two_weeks":
#         Project.objects.filter(pk=instance.id).update(duration = two_weeks())
#     if created and instance.dura_converter == "three_weeks":
#         Project.objects.filter(pk=instance.id).update(duration = three_weeks())
#     if created and instance.dura_converter == "one_month":
#         Project.objects.filter(pk=instance.id).update(duration = one_month())
        

# @receiver(post_save, sender=Project)
# def extend_deadline_of_project(sender, instance, created, **kwargs):
#     if instance.action == True and instance.dura_converter == "one_day":
#         Project.objects.filter(pk=instance.id).update(action = False, duration = one_day())
#     if instance.action == True and instance.dura_converter == "two_days":
#         Project.objects.filter(pk=instance.id).update(action = False, duration = two_days())
#     if instance.action == True and instance.dura_converter == "three_days":
#         Project.objects.filter(pk=instance.id).update(action = False, duration = three_days())
#     if instance.action == True and instance.dura_converter == "four_days":
#         Project.objects.filter(pk=instance.id).update(action = False, duration = four_days())
#     if instance.action == True and instance.dura_converter == "five_days":
#         Project.objects.filter(pk=instance.id).update(action = False, duration = five_days())
#     if instance.action == True and instance.dura_converter == "six_days":
#         Project.objects.filter(pk=instance.id).update(action = False, duration = six_days())
#     if instance.action == True and instance.dura_converter == "one_week":
#         Project.objects.filter(pk=instance.id).update(action = False, duration = one_week())
#     if instance.action == True and instance.dura_converter == "two_weeks":
#         Project.objects.filter(pk=instance.id).update(action = False, duration = two_weeks())
#     if instance.action == True and instance.dura_converter == "three_weeks":
#         Project.objects.filter(pk=instance.id).update(action = False, duration = three_weeks())
#     if instance.action == True and instance.dura_converter == "one_month":
#         Project.objects.filter(pk=instance.id).update(action = False, duration = one_month())
        












