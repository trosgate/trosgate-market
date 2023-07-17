from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse


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
		verbose_name = _("Plugin -Site")
		verbose_name_plural = _("Plugins -Site")

	def __str__(self):
		return self.preview
	

class PluginFeature(models.Model):
    title = models.CharField(max_length=100, unique=True)
    preview = models.TextField(_("Preview"), max_length=1000, blank=True, null=True)
    promo_image = models.ImageField(_("Promo Image"), upload_to='promo/', default='home_promo.jpg')
    feature1 = models.CharField(_("Feature1"), max_length=255, blank=True, null=True)
    feature2 = models.CharField(_("Feature2"), max_length=255, blank=True, null=True)
    feature3 = models.CharField(_("Feature3"), max_length=255, blank=True, null=True)
    feature4 = models.CharField(_("Feature4"), max_length=255, blank=True, null=True)
    feature5 = models.CharField(_("Feature5"), max_length=255, blank=True, null=True)
    feature6 = models.CharField(_("Feature6"), max_length=255, blank=True, null=True)
    ordering = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ('ordering',)
        verbose_name = _("Plugin Feature")
        verbose_name_plural = _("Plugins Features")
        
    def __str__(self):
        return str(self.title)   


class Plugin(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    price = models.PositiveIntegerField(_("Price"),)
    preview = models.TextField(_("Preview"), max_length=750)
    description = models.TextField(_("Description"), max_length=3500)
    mode = models.BooleanField(_("Payment Mode"), choices=((False, 'One Time'), (True, 'Monthly')), default=False)
    status = models.BooleanField(default=True)
    feature = models.ManyToManyField(PluginFeature, verbose_name=_("Plugin feature"), related_name="features")
    created_at = models.DateTimeField(auto_now_add=True)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('ordering',)
        verbose_name = _("Plugin - Merchant")
        verbose_name_plural = _("Plugins - Merchant")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Plugin, self).save(*args, **kwargs)

    def __str__(self):
        return self.name	

    # absolute url for proposal detail page
    def plugin_absolute_url(self):
        return reverse('plugins:plugin_detail', kwargs={'plugin_slug':self.slug})
    

