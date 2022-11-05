# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from . models import Freelancer, FreelancerAccount
# from account. models import Customer
# from payments.models import PaymentAccount
# from teams.models import Package, Team, Invitation
# from django.utils.text import slugify


# @receiver(post_save, sender=Customer)
# def create_freelancer_profile(sender, instance, created, **kwargs):
#     '''
#     Create a freelancer profile ..
#     For user who signup as freelancer
#     '''
#     if created and instance.user_type == Customer.FREELANCER:
#         freelancer_profile = Freelancer.objects.create(user=instance)
#         freelancer_profile.save()
    
#         freelancer_account = FreelancerAccount.objects.create(user=instance)
#         freelancer_account.save()

#         freelancer_payment_account = PaymentAccount.objects.create(user=instance)
#         freelancer_payment_account.save()

#         try:
#             package = Package.objects.get(pk=1, type='Basic')
#         except Exception as e:
#             print(str(e))
#             package = Package.objects.create(pk=1, type='Basic')

#         try:
#             team = Team.objects.create(
#                 # status = "inactive" until signup is confirmed
#                 title=instance.short_name,
#                 notice="This is my first team", 
#                 created_by = instance,
#                 package = package,
#                 package_status = Team.DEFAULT,
#                 status = 'active'
#             )
#             team.slug = slugify(instance.short_name)
#             team.save()
#             team.members.add(instance)

#             freelancer = freelancer_profile
#             freelancer.active_team_id = team.id
#             freelancer.save()

#             invitation = Invitation.objects.create(
#                 team = team, 
#                 sender = instance, 
#                 email = instance.email, 
#                 type = 'founder',
#                 status = 'accepted'
#             )
#             invitation.save()
#         except Exception as e:
#             print(str(e))


















