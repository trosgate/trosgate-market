from django.db import models
from django.utils.translation import gettext_lazy as _


class FutureRelease(models.Model):
	preview = models.CharField(max_length=100, default='Your future in your hands to control', blank=True)
	alert  = models.CharField(max_length=100, default='Some of these features require additional settings. Be guided by the comments', blank=True)
    # Custom Features
	more_team_per_user = models.BooleanField(_("Teams Builder Plus"), 
    	choices = ((False,'Disabled'), (True, 'Launched')),
    	help_text=(_("By default, each freelancer is created with single Team. Same team can be upgraded. This plugin enables freelancer to create unlimited Teams and invite user to any of them. Also, newly created team have ability to upgrade")),  
    	default=True, 
    	blank=True
    )
	ext_contract = models.BooleanField(_("External Contract"), 
    	choices = ((False,'Disabled'), (True, 'Launched')),  
    	help_text=(_("This feature allows freelancer to add their own clients(from outside your platform). Then create contracts and link to those clients for them to receive mail and checkout after signup")), 
    	default=True, 
    	blank=True
    )

	deposit = models.BooleanField(_("Client Deposit"), 
    	choices = ((False,'Disabled'), (True, 'Launched')),
    	help_text=(_("With direct checkout flow, client will pay for services on the fly(direct). This plugin allows client to deposit first, and use it to purchase any service within the platform")),  
    	default=True, 
    	blank=True
    )
	transfer = models.BooleanField(_("Fund splitter/Transfer"), 
    	choices = ((False,'Disabled'), (True, 'Launched')),
    	help_text=(_("By default, service payments go to Team founder and freelancer Team members must pay themselves outside platform. If team is upgraded, Team founder can take advantage of this Plugin to pay other Team members on platform")),  
    	default=True, 
    	blank=True
    )

	sms_authenticator = models.BooleanField(_("2FA Mailer"), 
    	choices = ((False,'Disabled'), (True, 'Launched')), 
    	default=True,
    	help_text=(_("By default, all users(excluding Staff) will be able to login to dashoard using EMAIL and PASSWORD. This plugin will (1) Present extra Token form after login, (2) Send simple mail alert containingg token, (3) button to resend token if customer has not received, (4) Then a valid token entered will log user to dashboard")), 
    	blank=True
    )

	class Meta:
		verbose_name = _("Plugin")
		verbose_name_plural = _("Plugins")

	def __str__(self):
		return self.preview