from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from account.tokens import account_activation_token
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from general_settings.backends import get_from_email
from general_settings.models import WebsiteSetting
from general_settings.utilities import (
    website_name,
    get_protocol_with_domain_path,
    get_instagram_path, 
    get_facebook_path, 
    get_youtube_path, 
    get_twitter_path
)

#
# Utility function for sending Test email using celery
def send_test_mail(to_email):
    from_email = get_from_email()
    subject = f'Test Email on {website_name()}'
    text_content = f"Test Email on {website_name()}"
    html_content = render_to_string('notification/test_email.html', {
        'website_email': from_email,
        'text_content': text_content,
        'website_name': website_name(),
    })
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#
# Utility function for sending login token via mail
def two_factor_auth_mailer(user, pass_code):
    from_email = get_from_email()
    subject = f'User login activation on {website_name()}'
    text_content = f"Hello {user.short_name}, You are about to log into your account. Please your code for login on {website_name()} is: { pass_code}"
    html_content = render_to_string('notification/two_factor_auth.html', {
        'website_email': from_email,
        'website_name': website_name(),
        'user': user.short_name,
        'subject': subject,
        'pass_code': pass_code,
       
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


#
# Utility function for sending new signup
def new_user_registration(user):
    from_email = get_from_email()
    subject = 'Activate your Account'
    subtitle = f'Welcome to {website_name()}'
    text_content = f'Welcome to {website_name()}'
    message = f"Welcome to {website_name()}. You are almost ready to get started. Please click on the button below to verify your email address and enjoy exclusive services with us! Link has expiration so please make hay"
    html_content = render_to_string('notification/account_activation_mail.html', {
        'website_email': from_email,
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
        'user': user,
        'subtitle': subtitle,
        'subject': subject,
        'message': message,
        'encode_id': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),        
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# Utility function for notifying project creator of new application
def application_notification(application):
    from_email = get_from_email()
    subject = 'Application received on your Project'
    subtitle = f'Your Project has new Application'
    text_content = f'Your Project on {website_name()} received new Application'
    html_content = render_to_string('notification/application_notification.html', {
        'website_email': from_email,
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
        'subtitle': subtitle,
        'application': application,
       
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [application.project.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


#Yet to test this.....................................
def credit_pending_balance_email(account, paid_amount, purchase):
    # Blueprint for sending mail when checkout is complete
    from_email = get_from_email()
    subject = f'Congrats. Your proposal was purchased'
    preview = f'Proposal paid for {paid_amount}'
    text_content = f'A New Checkout was paid_amount.'
    html_content = render_to_string('notification/credit_pending_balance_for_sales.html', {
        'subject': subject,
        'preview': preview,
        'account': account,
        'purchase': purchase,
        'paid_amount': paid_amount,
        # 'mywebsite': website(),
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [account.user.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def lock_fund_email(account, message):
    # Blueprint for sending mail when freelancer fund is locked
    from_email = get_from_email()
    subject = f'Account action taken by {website_name()}'
    preview = f'Temporal Lock on account - {account.user.get_full_name()}'
    text_content = f'Temporal Lock on your Fund account. Please check back later when we might have unlocked'
    html_content = render_to_string('notification/lock_fund_email.html', {
        'subject': subject,
        'preview': preview,
        'account': account,
        'message': message,
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [account.user.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_marked_paid_in_bulk_email(payout):
    # Blueprint for sending mail when payment is marked by admin
    from_email = get_from_email()
    # acceptation_url = settings.WEBSITE_URL
    subject = f'Your withdrawal Ref {payout.reference} was Approved'
    preview = f'Payout Ref {payout.reference} was Approved'
    text_content = f'Invitation to {payout.team.title}.'
    html_content = render_to_string('notification/withdrawal_marked_as_paid.html', {
        'subject': subject,
        'preview': preview,
        'payout': payout,
        # 'mywebsite': website(),
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [payout.team.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_contract_accepted_email(contract):
    # Blueprint for sending mail when payment is marked by admin
    from_email = get_from_email()
    subject = f'Your offered Contract was Accepted'
    preview = f'Contract Ref {contract.reference} was Approved'
    text_content = f'Contract Ref {contract.reference} was Approved'
    html_content = render_to_string('notification/contract_accepted_email.html', {
        'subject': subject,
        'preview': preview,
        'contract': contract,
        # 'mywebsite': website(),
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),        
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [contract.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_contract_rejected_email(contract):
    # Blueprint for sending mail when payment is marked by admin
    from_email = get_from_email()
    subject = f'Your offered Contract was Rejected'
    preview = f'Contract Ref {contract.reference} was Rejected'
    text_content = f'Contract Ref {contract.reference} was Rejected'
    html_content = render_to_string('notification/contract_rejected_email.html', {
        'subject': subject,
        'preview': preview,
        'contract': contract,
        # 'mywebsite': website(),
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),        
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [contract.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_withdrawal_marked_failed_email(payout):
    # Blueprint for sending mail when payment error occured
    from_email = get_from_email()
    # acceptation_url = settings.WEBSITE_URL
    subject = f'Your withdrawal Ref {payout.reference} Failed'
    preview = f'Payout Ref {payout.reference} was not processed'
    text_content = f'Your withdrawal with Ref: {payout.reference} Failed.'
    html_content = render_to_string('notification/withdrawal_request_declined.html', {
        'payout': payout,
        'preview': preview,
        # 'mywebsite': website(),
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [payout.team.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def initiate_credit_memo_email(credit_memo):
    # Blueprint for sending mail to superuser
    from_email = get_from_email()
    subject = 'Freelancer Credit Memo Initiated'
    text_content = f'New memo initiated for freelancer credit.'
    html_content = render_to_string('notification/initiate_credit_memo_email.html', {
        'subject': subject,
        'account': credit_memo,
        # 'mywebsite': website(),
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),        
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [credit_memo.sender.email,credit_memo.receiver.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def send_credit_to_team(account):
    # Blueprint for sending mail to receiver of new credit given by admin
    from_email = get_from_email()
    subject = 'You have received a Credit'
    text_content = f'Invitation to {account.team.title}.'
    html_content = render_to_string('notification/new_credit_email.html', {
        'account': account,
        'team': account.team,
        # 'mywebsite': website(),
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),        
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [account.team.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def new_ticket_email(ticket):
    # Blueprint for sending mail when new ticket created
    from_email = get_from_email()
    # acceptation_url = settings.WEBSITE_URL
    subject = f'New Ticket {ticket.reference} created'
    preview = f'Ticket No. {ticket.reference} created'
    text_content = f'A New Checkout was paid_amount.'
    html_content = render_to_string('notification/new_ticket_email.html', {
        'preview': preview,
        'ticket': ticket,
        # 'mywebsite': website(),
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [ticket.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def ticket_reply_email(ticketreply):
    # Blueprint for sending mail when ticket replied by support
    from_email = get_from_email()
    # acceptation_url = settings.WEBSITE_URL
    subject = f'Ticket number {ticketreply.ticket.reference} replied'
    preview = f'Ticket No: {ticketreply.ticket.reference} replied'
    text_content = f'A New Checkout was paid_amount.'
    html_content = render_to_string('notification/ticket_reply.html', {
        'preview': preview,
        'ticketreply': ticketreply,
        # 'mywebsite': website(),
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [ticketreply.ticket.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def application_cancel_email(message):
    # Blueprint for sending mail when application is cancelled
    from_email = get_from_email()
    subject = f'Job cancellation request'
    preview = f'A dispute has been raised. Take action'
    text_content = f'A New Checkout was paid_amount.'
    html_content = render_to_string('notification/application_cancel_email.html', {
        'message': message,
        'preview': preview,
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [message.resolution.application.team.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def approve_application_cancel_email(resolution):
    # Blueprint for sending mail when application is cancelled
    from_email = get_from_email()
    subject = f'Your Cancellation Request Approved'
    preview = f'Payment reversed to your Account'
    text_content = f'A New Checkout was paid_amount.'
    html_content = render_to_string('notification/approve_application_cancel_email.html', {
        'resolution': resolution,
        'preview': preview,
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [resolution.application.purchase.client.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()



# To be continued
# To be continued
# To be continued
# To be continued
# To be continued
def send_new_team_email(to_email, team):
    from_email = get_from_email()
    # acceptation_url = settings.WEBSITE_URL
    subject = 'Activate your Team'
    text_content = f'Invitation to {team.title}.'
    html_content = render_to_string('teams/new_team_email.html', {
        'team': team,
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# Utility function for sending envites to team
def send_invitation_email(to_email, code, team):
    from_email = get_from_email()
    # acceptation_url = settings.WEBSITE_URL
    subject = 'Invitation to Team'
    text_content = f'Invitation to {team.title}. Your code is: %s' % code
    html_content = render_to_string('notification/email_invitation.html', {
        'team': team,
        'code': code,
        # 'protocol': Protocol,
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#
# Utility function for notifying team founder when envites accept your invitation

def send_invitation_accepted_mail(team, invitation):
    from_email = get_from_email()
    subject = 'Invitation accepted'
    text_content = 'Your invitation was accepted'
    context={
        'team': team, 
        'invitation': invitation,
        'website_name': website_name(),
        'protocol_with_domain': get_protocol_with_domain_path(),
        'instagram_path': get_instagram_path(),
        'facebook_path': get_facebook_path(),
        'youtube_path': get_youtube_path(),
        'twitter_path': get_twitter_path(),        
    }
    html_content = render_to_string('notification/accept_invitation_email.html', context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [team.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

