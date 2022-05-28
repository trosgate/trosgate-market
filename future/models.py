from django.db import models
from django.utils.translation import gettext_lazy as _


class FutureRelease(models.Model):
	preview = models.CharField(max_length=100, default='Your future in your hands to control', blank=True)
	alert  = models.CharField(max_length=100, default='Some of these features require additional settings. Be guided by the comments', blank=True)
    # Custom Features
	more_team_per_user = models.BooleanField(_("More Teams per Freelancer"), 
    	choices = ((False,'Disabled'), (True, 'Launched')),
    	help_text=(_("By default, each freelancer is created with one Team. This feature enables freelancer to create unlimited Teams and invite user to any of them")),  
    	default=True, 
    	blank=True
    )
	ext_contract = models.BooleanField(_("External Contract"), 
    	choices = ((False,'Disabled'), (True, 'Launched')),  
    	help_text=(_("This feature allows freelancer to add their own clients(from outside your platform). Then create contracts and link to those clients for them to receive mail and checkout without login")), 
    	default=True, 
    	blank=True
    )

	deposit = models.BooleanField(_("Client Deposit"), 
    	choices = ((False,'Disabled'), (True, 'Launched')),
    	help_text=(_("In addition to the generic flow where client will pay for services on the fly, this feature allows client to deposit first, and use it to purchase any service")),  
    	default=True, 
    	blank=True
    )
	transfer = models.BooleanField(_("Gift/Transfer"), 
    	choices = ((False,'Disabled'), (True, 'Launched')),
    	help_text=(_("By default, freelancer Team members must pay themselves outside platform. Team founder can take advantage of this Gift/Transfer feature to pay other Team members on platform")),  
    	default=True, 
    	blank=True
    )

	sms_authenticator = models.BooleanField(_("2FA SMS Auth"), 
    	choices = ((False,'Disabled'), (True, 'Launched')), 
    	default=True,
    	help_text=(_("This will only work if you first setup Twilio credentials in dashboard under settings. If launched, freelancer and client will be required to verify login by SMS")), 
    	blank=True
    )


	class Meta:
		verbose_name = _("Future Release")
		verbose_name_plural = _("Future Releases")

	def __str__(self):
		return self.preview