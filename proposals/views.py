import random
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proposal, ProposalChat
from teams.models import Team
from django.contrib.auth.decorators import login_required
from .forms import ProposalStepOneForm, ProposalStepTwoForm, ProposalStepThreeForm, ProposalStepFourForm, ProposalChatForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from freelancer.models import Freelancer
from account.permission import user_is_freelancer
from general_settings.models import Category, Skill
from django.contrib import auth, messages
from django.views.decorators.cache import cache_control #prevent back button on browser after form submission
from account.models import Country, Merchant
from django.template.loader import render_to_string
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from teams.controller import PackageController
from account.models import Customer
from client.models import Client
from resolution.reviews import (
    proposal_review_average, 
    contract_review_average,
)
from resolution.models import (ApplicationReview, ProposalReview, ContractReview)
from analytics.analytic import (
    proposal_sales_count_by_proposal,
    proposal_sales_count_by_contract,
)
from django.db.models import Sum, Avg, Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.sites.shortcuts import get_current_site



def merchant_proposal(request):
    proposals = Proposal.objects.filter(merchant__site=request.user.merchant.site.id)
    
    active_proposals = proposals.filter(status='active').count()
    review_proposals = proposals.filter(status='review').count()
    published_proposals = proposals.filter(published=True).count()
    unpublished_proposals = proposals.filter(published=False).count()
    
    total_proposal = f'{proposals} found for the search'
    
    context = {
        "proposals": proposals,
        "total_proposal": total_proposal,
        "active_proposals":active_proposals, 
        "review_proposals":review_proposals, 
        "published_proposals":published_proposals, 
        "unpublished_proposals":unpublished_proposals, 
    }
    return render(request, 'proposals/merchant_proposal.html', context)


def proposal_listing(request):
    categorie = Category.objects.filter(visible = True).distinct()
    countries = Country.objects.filter(supported = True).distinct()
    skills = Skill.objects.all().distinct()
    proposals = Proposal.objects.filter(status='active').distinct()
    
    base_currency = get_base_currency_symbol()
    all_proposals = proposals.count()
    
    totalcount = f'{all_proposals} found for the search'
    context = {
        "skills":skills, 
        "countries":countries, 
        "categorie":categorie, 
        "proposals": proposals,
        "base_currency": base_currency,
        "totalcount": totalcount
    }
    return render(request, 'proposals/proposal_listing.html', context)


def proposal_filter(request):
    base_currency = get_base_currency_symbol()
    #Country
    country = request.GET.getlist('country[]')
    # Category
    category = request.GET.getlist('category[]')
    # Skills
    skill = request.GET.getlist('skill[]')
    # Revision Status
    revision_true = request.GET.get('true[]', '')
    revision_false = request.GET.get('false[]', '')
    # Duration
    one_day = request.GET.get('one_day[]', '')
    two_days = request.GET.get('two_days[]', '')
    three_days = request.GET.get('three_days[]', '')
    four_days = request.GET.get('four_days[]', '')
    five_days = request.GET.get('five_days[]', '')
    six_days = request.GET.get('six_days[]', '')
    one_week = request.GET.get('one_week[]', '')
    two_weeks = request.GET.get('two_weeks[]', '')
    three_weeks = request.GET.get('three_weeks[]', '')
    one_month = request.GET.get('one_month[]', '')
    # Upgraded Teams
    upgraded_teams = request.GET.get('upgradedTeams[]', '')
    # Price Filter
    less_than_50_dollar = request.GET.get('less_than_50_dollar[]', '')
    fify_dollar_to_100_dollar = request.GET.get('fify_dollar_to_100_dollar[]', '')
    hundred_dollar_to_350_dollar = request.GET.get('hundred_dollar_to_350_dollar[]', '')
    three_fifty_dollar_to_500_dollar = request.GET.get('three_fifty_dollar_to_500_dollar[]', '')
    above_500_dollar = request.GET.get('above_500_dollar[]', '')

    proposals = Proposal.objects.all()
    all_proposals = proposals.count()
    #Country
    if len(country) > 0:
        proposals = proposals.filter(team__created_by__country__id__in=country).distinct()
    # Category    
    if len(category) > 0:
        proposals = proposals.filter(category__id__in=category).distinct()
    # Skills    
    if len(skill) > 0:
        proposals = proposals.filter(skill__id__in=skill).distinct()
    # Revision Status
    if revision_true != '':
        proposals = proposals.filter(revision=True).distinct()
    if revision_false != '':
        proposals = proposals.filter(revision=False).distinct()
    # Duration
    if one_day != '':
        proposals = proposals.filter(dura_converter = one_day).distinct()
    if two_days != '':
        proposals = proposals.filter(dura_converter = two_days).distinct()
    if three_days != '':
        proposals = proposals.filter(dura_converter = three_days).distinct()
    if four_days != '':
        proposals = proposals.filter(dura_converter = four_days).distinct()
    if five_days != '':
        proposals = proposals.filter(dura_converter = five_days).distinct()
    if six_days != '':
        proposals = proposals.filter(dura_converter = six_days).distinct()
    if one_week != '':
        proposals = proposals.filter(dura_converter = one_week).distinct()
    if two_weeks != '':
        proposals = proposals.filter(dura_converter = two_weeks).distinct()
    if three_weeks != '':
        proposals = proposals.filter(dura_converter = three_weeks).distinct()
    if one_month != '':
        proposals = proposals.filter(dura_converter = one_month).distinct()
    # Upgraded Teams
    if upgraded_teams != '':
        proposals = proposals.filter(team__package__type = 'Team').distinct()
    # Price Filter    
    if less_than_50_dollar != '':
        proposals = proposals.filter(salary__lte = 50).distinct()
    if fify_dollar_to_100_dollar != '':
        proposals = proposals.filter(salary__gte = 50, salary__lte=100).distinct()
    if hundred_dollar_to_350_dollar != '':
        proposals = proposals.filter(salary__gte = 100, salary__lte=350).distinct()
    if three_fifty_dollar_to_500_dollar != '':
        proposals = proposals.filter(salary__gte = 350, salary__lte=500).distinct()
    if above_500_dollar != '':
        proposals = proposals.filter(salary__gte=500).distinct()

    search_count = len(proposals)
    totalcount = f'<div id="proposalTotal" class="alert alert-info text-center" role="alert" style="color:black;">{search_count} of {all_proposals} search results found</div>'
    returned_proposal = render_to_string('proposals/partials/proposal_search.html', {'proposals':proposals, 'base_currency':base_currency})
    
    if len(proposals) > 0: 
        return JsonResponse({'proposals': returned_proposal, 'base_currency':base_currency, 'totalcount':totalcount})
    else:
        returned_proposal = f'<div class="alert alert-warning text-center" role="alert" style="color:red;"> Hmm! nothing to show for this search</div>'
        return JsonResponse({'proposals': returned_proposal, 'base_currency':base_currency, 'totalcount':totalcount})


@login_required
@user_is_freelancer
def create_proposal(request):
    proposalformone = ProposalStepOneForm(request.POST or None)
    initial_data = request.session.get('post_step_one', {})
    proposalformone = ProposalStepOneForm(initial=initial_data)
    return render(request, 'proposals/proposal_create.html', {'proposalformone': proposalformone, 'variable': 'stepOne'})


@login_required
@user_is_freelancer
def proposal_step_one(request):
    if request.method == 'POST':
        proposalformone = ProposalStepOneForm(request.POST or None)

        if proposalformone.is_valid():
            # Store form data in session
            step_one_data = {}
            step_one_data['title'] = proposalformone.cleaned_data['title']
            step_one_data['preview'] = proposalformone.cleaned_data['preview']
            step_one_data['category'] = proposalformone.cleaned_data['category'].pk
            request.session['post_step_one'] = step_one_data

            return redirect("proposals:proposal_step_two")
        
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Get initial form data from session if available
        initial_data = request.session.get('post_step_one', {})
        print('initial_data :', initial_data)
        proposalformone = ProposalStepOneForm(initial=initial_data)
    return render(request, 'proposals/partials/create_steps.html', {'proposalformone': proposalformone, 'variable': 'stepOne'})


@login_required
@user_is_freelancer
def proposal_step_two(request):
    # Get form data from previous step
    step_one_data = request.session.get('post_step_one')
    if not step_one_data:
        return redirect("proposals:proposal_step_one")
   
    if request.method == 'POST':
        proposalformtwo = ProposalStepTwoForm(request.POST)
        if proposalformtwo.is_valid():
            # Update session data with new form data
            request.session['post_step_two'] = proposalformtwo.cleaned_data
            step_one_data.update(proposalformtwo.cleaned_data)
            return redirect("proposals:proposal_step_three")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Get initial form data from session if available
        initial_data = request.session.get('post_step_two', {})
        proposalformtwo = ProposalStepTwoForm(initial=initial_data)
    return render(request, 'proposals/partials/create_steps.html', {'proposalformtwo': proposalformtwo, 'variable': 'stepTwo'})


@login_required
@user_is_freelancer
def proposal_step_three(request):
    # Get form data from previous steps
    step_one_data = request.session.get('post_step_one')
    step_two_data = request.session.get('post_step_two')
    
    if not step_one_data:
        return redirect("proposals:proposal_step_one")

    if not step_two_data:
        return redirect("proposals:proposal_step_two")
    
    if request.method == 'POST':
        proposalformthree = ProposalStepThreeForm(request.POST)
        if proposalformthree.is_valid():
            # Update session data with new form data
            request.session['post_step_three'] = proposalformthree.cleaned_data
            step_one_data.update(proposalformthree.cleaned_data)
            return redirect("proposals:proposal_step_four")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Get initial form data from session if available
        initial_data = request.session.get('post_step_three', {})
        proposalformthree = ProposalStepThreeForm(initial=initial_data)
    return render(request, 'proposals/partials/create_steps.html', {'proposalformthree': proposalformthree, 'variable': 'stepThree'})


@login_required
@user_is_freelancer
def proposal_step_four(request):
    # Get form data from previous steps
    step_one_data = request.session.get('post_step_one')
    step_two_data = request.session.get('post_step_two')
    step_three_data = request.session.get('post_step_three')
    
    if not step_one_data:
        return redirect("proposals:proposal_step_one")

    if not step_two_data:
        return redirect("proposals:proposal_step_two")
    
    if not step_three_data:
        return redirect("proposals:proposal_step_three")
     
    if request.method == 'POST':
        proposalformfour = ProposalStepFourForm(request.POST, request.FILES)
        if proposalformfour.is_valid():
            # unpack and combine all form data from previous steps and current step
            form_data = {**step_one_data, **step_two_data, **step_three_data, **proposalformfour.cleaned_data}
            # Create Post object
 
            category = get_object_or_404(Category, pk=form_data['category'])
            team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id)
            proposal = Proposal.objects.create(
                title=form_data['title'],
                preview=form_data['preview'],
                description=form_data['description'],
                sample_link=form_data['sample_link'],
                salary=form_data['salary'],
                service_level=form_data['service_level'],
                revision=form_data['revision'],
                dura_converter=form_data['dura_converter'],
                faq_one=form_data['faq_one'],
                faq_one_description=form_data['faq_one_description'],
                faq_two=form_data['faq_two'],
                faq_two_description=form_data['faq_two_description'],
                thumbnail=form_data['thumbnail'],
                category=category,
                created_by=request.user,
                team=team,
            )

            proposal.skill.set(proposalformfour.cleaned_data['skill'])
            proposal.slug = slugify(proposal.title)
            proposal.save()
            
            if proposal.pk:
                # Clear session data
                del request.session['post_step_one']
                del request.session['post_step_two']
                del request.session['post_step_three']

            return render(request, 'proposals/partials/create_steps.html', {'variable': 'stepFive', 'proposal':proposal})
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Get initial form data from session if available
        initial_data = request.session.get('post_step_four', {})
        proposalformfour = ProposalStepFourForm(initial=initial_data)
    return render(request, 'proposals/partials/create_steps.html', {'proposalformfour': proposalformfour, 'variable': 'stepFour'})


@login_required
@user_is_freelancer
def modify_proposals(request, proposal_id, proposal_slug):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)  
    proposal = get_object_or_404(Proposal, team=team, pk=proposal_id, slug=proposal_slug)

    proposalformone = ProposalStepOneForm(instance = proposal)           

    context = {
        'proposalformone': proposalformone,
        'proposal': proposal,
        'variable': 'stepOne'
    }
    return render(request, 'proposals/proposal_edit.html', context)


@login_required
@user_is_freelancer
def modify_proposal_step_one(request, proposal_id, proposal_slug):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)  
    proposal = get_object_or_404(Proposal, team=team, pk=proposal_id, slug=proposal_slug)

    proposalformone = ProposalStepOneForm(request.POST or None, instance=proposal)

    if proposalformone.is_valid():
        proposalformone.save()

        messages.info(request, 'Changed successfully.')

    else:
        proposalformone = ProposalStepOneForm(instance = proposal)           

    context = {
        'proposalformone': proposalformone,
        'proposal': proposal,
        'variable': 'stepOne'
    }
    return render(request, 'proposals/partials/modify_steps.html', context)


@login_required
@user_is_freelancer
def modify_proposal_step_two(request, proposal_id, proposal_slug):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)  
    proposal = get_object_or_404(Proposal, team=team, pk=proposal_id, slug=proposal_slug)

    proposalformtwo = ProposalStepTwoForm(request.POST or None, instance=proposal)

    if proposalformtwo.is_valid():
        proposalformtwo.save()

        messages.info(request, 'Changed successfully.')

    else:
        proposalformtwo = ProposalStepTwoForm(instance = proposal)           

    context = {
        'proposalformtwo': proposalformtwo,
        'proposal': proposal,
        'variable': 'stepTwo'        
    }
    return render(request, 'proposals/partials/modify_steps.html', context)


@login_required
@user_is_freelancer
def modify_proposal_step_three(request, proposal_id, proposal_slug):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)  
    proposal = get_object_or_404(Proposal, team=team, pk=proposal_id, slug=proposal_slug)

    proposalformthree = ProposalStepThreeForm(request.POST or None, instance=proposal)

    if proposalformthree.is_valid():
        proposalformthree.save()

        messages.info(request, 'Changed successfully.')

    else:
        proposalformthree = ProposalStepThreeForm(instance = proposal)           

    context = {
        'proposalformthree': proposalformthree,
        'proposal': proposal,
        'variable': 'stepThree'        
    }
    return render(request, 'proposals/partials/modify_steps.html', context)


@login_required
@user_is_freelancer
def modify_proposal_step_four(request, proposal_id, proposal_slug):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)  
    proposal = get_object_or_404(Proposal, team=team, pk=proposal_id, slug=proposal_slug)

    proposalformfour = ProposalStepFourForm(request.POST or None, request.FILES or None, instance=proposal)

    if proposalformfour.is_valid():
        proposalformfour.save()

        messages.info(request, 'Changed successfully')

    else:
        proposalformfour = ProposalStepFourForm(instance = proposal)           

    context = {
        'proposalformfour': proposalformfour,
        'proposal': proposal,
        'variable': 'stepFour'        
    }
    return render(request, 'proposals/partials/modify_steps.html', context)


#This page shows proposals with review status
@login_required
@user_is_freelancer
def review_proposal(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    proposal = team.proposalteam.filter(status = Proposal.REVIEW)

    context = {
        'team':team,
        'proposal':proposal,
    }
    return render(request, 'proposals/review_proposal.html', context)


@login_required
@user_is_freelancer
def active_proposal(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)    
    proposal = team.proposalteam.filter(status = Proposal.ACTIVE)

    context = {
        'team':team,
        'proposal':proposal,
    }
    return render(request, 'proposals/active_proposal.html', context)


@login_required
@user_is_freelancer
def archive_proposal_page(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)    
    proposal = team.proposalteam.filter(status = Proposal.ARCHIVE)

    context = {
        'team': team,
        'proposal': proposal,
    }
    return render(request, 'proposals/archived_proposal.html', context)


@login_required
@user_is_freelancer
def archive_proposal(request, short_name, proposal_slug):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    Proposal.objects.filter(team=team, created_by__short_name=short_name, slug=proposal_slug).update(status = Proposal.ARCHIVE)

    messages.success(request, 'The proposal was archived successfully!')

    return redirect('proposals:active_proposal')


@login_required
@user_is_freelancer
def reactivate_archive_proposal(request, short_name, proposal_slug):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    Proposal.objects.filter(team=team, created_by__short_name=short_name, slug=proposal_slug, status = Proposal.ARCHIVE).update(status = Proposal.ACTIVE)

    messages.success(request, 'The archived proposal was re-activated successfully!')

    return redirect('proposals:archive_proposal_page')


@login_required
@user_is_freelancer
def proposal_preview(request, short_name, proposal_slug):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    proposal = get_object_or_404(Proposal, slug=proposal_slug, created_by__short_name=short_name, team=team)
    profile_view = get_object_or_404(Freelancer, user=proposal.created_by)
    
    team_members = proposal.team.members.all()
        
    context = {
        "proposal": proposal,
        "team_members": team_members,
        "profile_view": profile_view,

    }
    return render(request, 'proposals/proposal_preview.html', context)


def proposal_detail(request, short_name, proposal_slug):
    proposal = get_object_or_404(Proposal, slug=proposal_slug, created_by__short_name=short_name, status = Proposal.ACTIVE)
    profile_view = get_object_or_404(Freelancer, user=proposal.created_by)   
    other_proposals = Proposal.active.exclude(pk=proposal.id)[:4]    
    team_members = proposal.team.members.all()

    proposal_review_msg = ProposalReview.objects.filter(
        resolution__proposal_sale__proposal__team=proposal.team, 
        resolution__proposal_sale__proposal=proposal,
        status = True
    )[:15]

    review_status = (proposal_review_msg.count() < 1)

    proposal_review_avg = proposal_review_average(proposal.team, proposal)
    contract_review_avg = contract_review_average(proposal.team, proposal)

    sales_count_by_proposal = proposal_sales_count_by_proposal(proposal.team, proposal)['sales_count']
    sales_count_by_contract = proposal_sales_count_by_contract(proposal.team, proposal)['sales_count'] 

    overal_proposal_sales_count = (
        sales_count_by_proposal+ 
        sales_count_by_contract
    )

    all_viewed_proposals = ''
    proposal_id = proposal.id
    session = request.session
    captured_proposal = ''
    sesion_proposal = ''

    if request.user.is_authenticated:
        if "recently_viewed" in request.session:
            if proposal_id in session["recently_viewed"]:
                session["recently_viewed"].remove(proposal.id)

            captured_proposal = Proposal.objects.filter(pk__in=session["recently_viewed"])
            all_viewed_proposals = sorted(captured_proposal, key=lambda x: session["recently_viewed"].index(x.id))
            session["recently_viewed"].insert(0, proposal.id)        
            if len(session["recently_viewed"]) > 5:
                session["recently_viewed"].pop()
       
        else:
            sesion_proposal = session["recently_viewed"] = [proposal.id]
    
    request.session.modified = True
    context = {
        'base_currency':get_base_currency_symbol(),
        "proposal": proposal,
        "overal_proposal_sales_count": overal_proposal_sales_count,
        "sales_count_by_proposal": sales_count_by_proposal,
        "sales_count_by_contract": sales_count_by_contract,
        "other_proposals": other_proposals,
        "team_members": team_members,
        "profile_view": profile_view,
        "proposal_review_avg": proposal_review_avg,
        "contract_review_avg": contract_review_avg,
        "proposal_review_msg":proposal_review_msg,
        "review_status":review_status,
        "sesion_proposal":sesion_proposal,
        "all_viewed_proposals":all_viewed_proposals,
    }
    if request.merchant.merchant.proposal_detail == False:
        return render(request, 'proposals/proposal_detail.html', context)
    else:
        return render(request, 'proposals/proposal_detail2.html', context)


@login_required
def proposal_chat_messages(request, proposal_slug):
    proposal=None
    if request.user.user_type == Customer.FREELANCER:    
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
        proposal = get_object_or_404(Proposal, slug=proposal_slug, team=team)

    elif request.user.user_type == Customer.CLIENT:
        proposal = get_object_or_404(Proposal, slug=proposal_slug)

    proposalchatform = ProposalChatForm()
    chats = ProposalChat.objects.filter(proposal=proposal, team=proposal.team)
    chat_count = chats.count()

    context = {
        'proposalchatform':proposalchatform,
        'proposal':proposal,
        'chats':chats,
        'chat_count':chat_count
    }

    return render(request, 'proposals/chat_messages.html', context)
    

@login_required
def create_message(request, proposal_id):
    proposal = get_object_or_404(Proposal, pk=proposal_id)
    chats = ProposalChat.objects.filter(proposal=proposal, team=proposal.team)

    content = request.POST.get('content', '')
    if content != '':
        ProposalChat.objects.create(
            content=content, 
            proposal=proposal,
            team=proposal.team, 
            sender=request.user
        )

    chat_count = chats.count()
    context = {
        'proposal':proposal,
        'chats':chats,
        'chat_count':chat_count
    }       
    return render(request, 'proposals/components/partial_proposal.html', context)


@login_required
def fetch_messages(request, proposal_id):
    proposal = get_object_or_404(Proposal, pk=proposal_id)
    chats = ProposalChat.objects.filter(proposal=proposal, team=proposal.team)

    context = {
        'proposal':proposal,
        'chats':chats,
    }
    return render(request, 'proposals/components/partial_proposal.html', context)

