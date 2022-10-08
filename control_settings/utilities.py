from general_settings.models import SubscriptionGateway, DepositGateway
from .models import LayoutSetting

def homepage_layout():
    if LayoutSetting.objects.filter(pk=1).exists():
        home_layout = LayoutSetting.objects.get(pk=1)
        return home_layout

    else:
        home_layout = LayoutSetting(
            pk=1, 
            title_block = "Hire Experts or Team",
            subtitle_block = "Consectetur adipisicing elit sed dotem eiusmod tempor incuntes ut labore etdolore maigna aliqua enim.",
            video_title = "See For Yourself!",
            video_description = "Hire Experts or Team",
            video_url = "https://youtu.be/vyMopYvFI4E",
            category_title = "Explore Categories",
            category_subtitle = "Professional by categories",
            proposal_title = "Explore Proposals",
            proposal_subtitle = "Verified Proposals",
            promo_title = "#1 Choice For Businesses",
            promo_subtitle = "Business on the Go",
            promo_description = "The Example Marketplace",
            promo_image = "freelancer/awards/banner.png",
            project_title = "Published Jobs",
            project_subtitle = "Apply and get Hired",
            footer_description = "Dotem eiusmod tempor incune utnaem labore etdolore maigna aliqua enim poskina ilukita ylokem lokateise ination voluptate velit esse cillum dolore eu fugiat nulla pariatur lokaim urianewce"
            )
        home_layout.save()
        return home_layout

def subscription_switch():
    if SubscriptionGateway.objects.filter(pk=1).exists():
        subscript_switcher = SubscriptionGateway.objects.get(pk=1)
        return subscript_switcher

    else:
        subscript_switcher = SubscriptionGateway(pk=1, paypal=True, stripe=True, razorpay=True, flutterwave=True).save()
        return subscript_switcher


def deposit_switch():
    if DepositGateway.objects.filter(pk=1).exists():
        depo_switcher = DepositGateway.objects.get(pk=1)
        return depo_switcher

    else:
        depo_switcher = DepositGateway(pk=1, paypal=True, stripe=True, razorpay=True, flutterwave=True).save()
        return depo_switcher
