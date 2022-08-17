from twisted.internet.protocol import Protocol
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from general_settings.backends import get_from_email
from general_settings.models import WebsiteSetting

#
# Utility function for sending envites to team

def website():
    try:
        return WebsiteSetting.objects.get(id=1)
    except:
         return None


def send_new_test_mail(to_email):
    # Blueprint for sending test mail
    from_email = get_from_email()
    subject = 'This is a test Email'
    message = 'This is a test Email to confirm that my email setup is fine'
    recipient_list = [to_email]
    html_message ='<h1> This is a test Email to confirm that my email setup is fine </h1>'

    send_mail(subject, message, from_email, recipient_list)

__all__ = ['send_new_test_mail']


#Yet to test this.....................................
def credit_pending_balance_email(account, paid_amount, purchase):
    # Blueprint for sending mail when checkout is complete
    from_email = get_from_email()
    acceptation_url = settings.WEBSITE_URL
    subject = f'Congrats. Your proposal was purchased'
    preview = f'Proposal paid for {paid_amount}'
    text_content = f'A New Checkout was paid_amount.'
    html_content = render_to_string('notification/credit_pending_balance_for_sales.html', {
        'subject': subject,
        'preview': preview,
        'account': account,
        'purchase': purchase,
        'paid_amount': paid_amount,
        'mywebsite': website(),
        'acceptation_url': acceptation_url,
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [account.user.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_marked_paid_in_bulk_email(payout):
    # Blueprint for sending mail when payment is marked by admin
    from_email = get_from_email()
    acceptation_url = settings.WEBSITE_URL
    subject = f'Your withdrawal Ref {payout.reference} was Approved'
    preview = f'Payout Ref {payout.reference} was Approved'
    text_content = f'Invitation to {payout.team.title}.'
    html_content = render_to_string('notification/withdrawal_marked_as_paid.html', {
        'subject': subject,
        'preview': preview,
        'payout': payout,
        'mywebsite': website(),
        'acceptation_url': acceptation_url,
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
        'mywebsite': website(),
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
        'mywebsite': website(),
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [contract.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_withdrawal_marked_failed_email(payout):
    # Blueprint for sending mail when payment error occured
    from_email = get_from_email()
    acceptation_url = settings.WEBSITE_URL
    subject = f'Your withdrawal Ref {payout.reference} Failed'
    preview = f'Payout Ref {payout.reference} was not processed'
    text_content = f'Your withdrawal with Ref: {payout.reference} Failed.'
    html_content = render_to_string('notification/withdrawal_request_declined.html', {
        'payout': payout,
        'preview': preview,
        'mywebsite': website(),
        'acceptation_url': acceptation_url,
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
        'mywebsite': website(),
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
        'mywebsite': website(),
        'team': account.team,
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [account.team.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

# To be continued
# To be continued
# To be continued
# To be continued
# To be continued
def send_new_team_email(to_email, team):
    from_email = get_from_email()
    acceptation_url = settings.WEBSITE_URL
    subject = 'Activate your Team'
    text_content = f'Invitation to {team.title}.'
    html_content = render_to_string('teams/new_team_email.html', {
        'protocol': Protocol,
        'team': team,
        'acceptation_url': acceptation_url,
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# Utility function for sending envites to team
def send_invitation_email(to_email, code, team):
    from_email = get_from_email()
    acceptation_url = settings.WEBSITE_URL
    subject = 'Invitation to Team'
    text_content = f'Invitation to {team.title}. Your code is: %s' % code
    html_content = render_to_string('teams/email_invitation.html', {
        'protocol': Protocol,
        'team': team,
        'code': code,
        'acceptation_url': acceptation_url,
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
        'invitation': invitation
    }
    html_content = render_to_string('teams/accept_invitation_email.html', context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [team.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
