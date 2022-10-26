from django.shortcuts import render, redirect, get_object_or_404
from .models import Announcement, Blog, HelpDesk, Ticket, TicketMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .forms import TicketForm, CustomerTicketReplyForm, TicketStatesForm
from account.models import Customer
from teams.models import Team
from django.http import JsonResponse
from account.fund_exception import GenException


@login_required
def notice(request):
    notices = Announcement.objects.all()[:5]
    context ={
        'notices':notices
    }
    return render(request, 'marketing/notice.html', context)


def article_list(request):
    all_blogs  = Blog.objects.filter(published=True)
    freelancer_blogs = Blog.objects.filter(published=True, type=Blog.FREELANCER)
    client_blogs = Blog.objects.filter(published=True, type=Blog.CLIENT)

    context ={
        "all_blogs":all_blogs,
        "freelancer_blogs":freelancer_blogs,
        "client_blogs":client_blogs
    }
    return render( request, "marketing/blog_list.html", context)


def article_detail(request, article_slug):
    blog = get_object_or_404(Blog, slug=article_slug, published=True)

    context ={
        "blog":blog,
    }
    return render( request, "marketing/blog_detail.html", context)


@login_required
def ticket_and_support(request):
    support = ''

    for supports in HelpDesk.objects.filter(published=True):
        support = supports
    all_support = support

    ticketform = TicketForm()

    context ={
        "support":all_support,
        "ticketform":ticketform,
    }
    return render( request, "marketing/ticket_and_support.html", context)


@login_required
def create_ticket(request):
    team = None
    message = ''
    error = ''
    response = ''

    if request.POST.get('action') == 'create-ticket':
        title = str(request.POST.get('ticketTitle'))
        query_type = str(request.POST.get('ticketQuery_type'))
        product_type = str(request.POST.get('ticketProduct_type'))
        product_reference = str(request.POST.get('ticketProduct_Reference', ''))
        content = str(request.POST.get('ticketContent'))

        if request.user.user_type == Customer.FREELANCER:
            team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user])
        
            try:
                Ticket.create(
                    created_by=request.user,
                    title=title, 
                    content=content, 
                    query_type=query_type, 
                    product_type=product_type,
                    product_type_reference=product_reference,
                    team=team, 
                )
                message = f'The ticket was created successfuly'
    
            except GenException as e:
                error = str(e)
            response = JsonResponse({'message': message, 'error': error})
            return response

        elif request.user.user_type == Customer.CLIENT:
            try:
                Ticket.create(
                    created_by=request.user, 
                    title=title,
                    content=content, 
                    query_type=query_type, 
                    product_type=product_type,
                    product_type_reference=product_reference,
                )
                message = f'The ticket was created successfuly'
    
            except GenException as e:
                error = str(e)
        
            response = JsonResponse({'message': message, 'error': error})
            return response


@login_required
def customer_ticket_list(request):
    tickets = None
    team = None
    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
        tickets = Ticket.objects.filter(team=team)[:20]

    elif request.user.user_type == Customer.CLIENT:
        tickets = Ticket.objects.filter(created_by=request.user)[:20]

    context ={
        "tickets":tickets,
    }
    return render( request, "marketing/ticket_list.html", context)


@login_required
def customer_ticket_detail(request, ticket_id, ticket_slug):
    team = None
    reply = ''
    replies = ''

    if request.user.user_type == Customer.FREELANCER:
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, status=Team.ACTIVE)
        ticket = get_object_or_404(Ticket, pk=ticket_id, slug=ticket_slug, team=team)
        replies = ticket.tickettracker.all().order_by('-id')

        statusform = TicketStatesForm(request.POST or None, instance=ticket)
        replyform = CustomerTicketReplyForm(request.POST or None)
        if replyform.is_valid() and statusform.is_valid():
            reply = replyform.save(commit=False)
            reply.ticket = ticket
            reply.action = False
            reply.save()

            statusform.save()

            messages.info(request, 'The Ticket was replied successfully')
            return redirect('marketing:customer_ticket_detail', ticket_id=ticket.id, ticket_slug=ticket.slug)

    elif request.user.user_type == Customer.CLIENT:
        ticket = get_object_or_404(Ticket, pk=ticket_id, slug=ticket_slug, created_by=request.user)
        replies = ticket.tickettracker.all().order_by('-id')
        
        statusform = TicketStatesForm(request.POST or None, instance=ticket)
        replyform = CustomerTicketReplyForm(request.POST or None)

        if replyform.is_valid() and statusform.is_valid():
            reply = replyform.save(commit=False)
            reply.ticket = ticket
            reply.action = False
            reply.save()

            statusform.save()

            messages.info(request, 'The Ticket was replied successfully')
            return redirect('marketing:customer_ticket_detail', ticket_id=ticket.id, ticket_slug=ticket.slug)
           
    context ={
        "ticket":ticket,
        "replies":replies,
        "replyform":replyform,
        "statusform":statusform,
    }
    return render( request, "marketing/ticket_detail.html", context)










































