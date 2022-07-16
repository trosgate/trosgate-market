from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from client.models import Client
from account. models import Customer
from teams.models import Team, Invitation, Package
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from teams . utilities import create_random_code


code = create_random_code()[:6] 

@receiver(post_save, sender=Customer)
def create_default_team_and_package_and_invitation(sender, instance, created, **kwargs):
    '''
    for a new user(freelancer) with inactive status:
        Create a default team for the newly registered user
        set the team to inactive
        assign the freelancer profile of team owner to the team created
        set the package for that team to inactive
        set invitation status to Invited

    '''    
    if created and instance.is_active == False and instance.user_type == Customer.FREELANCER:
        package = Package.objects.get(pk=1) #this represents the basic package
        team = Team.objects.create(
            title=instance.short_name,
            notice="this is the basic team", 
            created_by = instance,
            package = package,
            package_status = Team.DEFAULT,
            slug = slugify(instance.short_name)
        )
        team.save()
        team.members.add(team.created_by)
        
        email = team.created_by.email
        freelancer = team.created_by.freelancer
        freelancer.active_team_id = team.id
        freelancer.save()

        invitation = Invitation.objects.create(team=team, sender=instance, email=email, type=Invitation.INTERNAL)
        invitation.save()


@receiver(post_save, sender=Customer)
def update_default_team_and_package_and_invitation(sender, instance, created, **kwargs):
    '''
    for a new user with active status:
        update the default team for the newly registered user
        set the team to active
        set the package for that team to active
        set invitation status to Accepted

    '''    
    if not created and instance.is_active == True and instance.user_type == Customer.FREELANCER:
        package = Package.objects.get(id=1)
        team = Team.objects.filter(
            title=instance.short_name, 
            created_by=instance, 
            status = Team.ACTIVE, 
            package = package, 
            package_status = Team.DEFAULT,
        )
        team.update(status = Team.ACTIVE)

        invitation = Invitation.objects.filter(email=instance.email, sender=instance, team__package=package, status = Invitation.INVITED)
        invitation.update(status = Invitation.ACCEPTED)


@receiver(post_save, sender=Package)
def maintain_state_of_the_two_packages(sender, instance, created, **kwargs):
    Package.objects.filter(id=1, type='Basic').update(max_member_per_team=1, price=0, is_default=True)        
    Package.objects.filter(id=2, type='Team').update(is_default=False)        
