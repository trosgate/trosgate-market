import random
import mimetypes

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proposal, ProposalProduct, ProposalChat
from teams.models import Team
from django.contrib.auth.decorators import login_required
from .forms import (
    ProposalStepOneForm, 
    ProposalStepTwoSingleForm, 
    ProposalStepTwoTierForm,
    ProposalStepThreeForm, 
    ProposalStepFourForm, 
    ProposalChatForm,
    ProposalProductForm
)
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from freelancer.models import Freelancer
from account.permission import user_is_freelancer, user_is_client
from general_settings.models import Category, Skill
from django.contrib import auth, messages
from django.views.decorators.cache import cache_control #prevent back button on browser after form submission
from account.models import Country, Merchant
from django.template.loader import render_to_string
from general_settings.currency import get_base_currency_symbol, get_base_currency_code
from account.models import Customer
from client.models import Client
from resolution.reviews import (
    proposal_review_average, 
    contract_review_average,
)
# from resolution.models import (ApplicationReview, ProposalReview, ContractReview)
from analytics.analytic import (
    proposal_sales_count_by_proposal,
    proposal_sales_count_by_contract,
)
from django.db.models import Sum, Avg, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import JsonResponse, FileResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.sites.shortcuts import get_current_site
from transactions.hiringbox import HiringBox
from django.db import transaction as db_transaction


def merchant_proposal(request):
    proposals = Proposal.objects.select_related('created_by','category','team').filter(merchant_id=request.user.merchant.id)
    
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
    proposals = Proposal.objects.select_related('category','team', 'created_by').filter(status='active').distinct()
    
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

    proposals = Proposal.objects.select_related('category','team', 'created_by').filter(
        merchant=request.merchant
    )
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
        proposals = proposals.filter(duration = one_day).distinct()
    if two_days != '':
        proposals = proposals.filter(duration = two_days).distinct()
    if three_days != '':
        proposals = proposals.filter(duration = three_days).distinct()
    if four_days != '':
        proposals = proposals.filter(duration = four_days).distinct()
    if five_days != '':
        proposals = proposals.filter(duration = five_days).distinct()
    if six_days != '':
        proposals = proposals.filter(duration = six_days).distinct()
    if one_week != '':
        proposals = proposals.filter(duration = one_week).distinct()
    if two_weeks != '':
        proposals = proposals.filter(duration = two_weeks).distinct()
    if three_weeks != '':
        proposals = proposals.filter(duration = three_weeks).distinct()
    if one_month != '':
        proposals = proposals.filter(duration = one_month).distinct()
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
        proposalformone = ProposalStepOneForm(initial=initial_data)
    return render(request, 'proposals/partials/create_steps.html', {'proposalformone': proposalformone, 'variable': 'stepOne'})


@login_required
@user_is_freelancer
def proposal_step_two(request):
    # Get form data from previous step
    step_one_data = request.session.get('post_step_one')
    pricing_type_data = request.session.get('pricing_data_type')
    
    if pricing_type_data is None:
        pricing_type_data = True   
        request.session['pricing_data_type'] = pricing_type_data

    if not step_one_data:
        return redirect("proposals:proposal_step_one")
 
    proposalform = ProposalStepTwoTierForm(request.POST or None)
    if pricing_type_data == False:
        proposalform = ProposalStepTwoSingleForm(request.POST or None)

    if request.method == 'POST':
        proposalformtwo = proposalform
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
        
        proposalformtwo = ProposalStepTwoTierForm(initial=initial_data)
        if pricing_type_data == False:
            proposalformtwo = ProposalStepTwoSingleForm(initial=initial_data)
            
    context = {
        'variable': 'stepTwo',
        'proposalformtwo': proposalformtwo, 
        'pricing_type_data': pricing_type_data
    }
    return render(request, 'proposals/partials/create_steps.html', context)


@login_required
@user_is_freelancer
def pricing_type(request):
    pricing_type_data = request.session.get('pricing_data_type')

    if  pricing_type_data == True:
        pricing_type_data = False
    elif  pricing_type_data == False:
        pricing_type_data = True
    else:
        pricing_type_data = True
    
    request.session['pricing_data_type'] = pricing_type_data
    initial_data = request.session.get('post_step_two', {})

    proposalformtwo = ProposalStepTwoTierForm(initial=initial_data)
    if pricing_type_data == False:
        proposalformtwo = ProposalStepTwoSingleForm(initial=initial_data)
           
    context = {
        'variable': 'stepTwo',
        'proposalformtwo': proposalformtwo, 
        'pricing_type_data': pricing_type_data
    }
    return render(request, 'proposals/partials/pricing_type.html', context)


@login_required
@user_is_freelancer
def proposal_step_three(request):
    # Get form data from previous steps
    step_one_data = request.session.get('post_step_one')
    step_two_data = request.session.get('post_step_two')
    pricing_type_data = request.session.get('pricing_data_type')
    
    if not step_one_data:
        return redirect("proposals:proposal_step_one")
    
    if not step_two_data:
        return redirect("proposals:proposal_step_two")
    
    if pricing_type_data is None:
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
    proposal = None
    step_one_data = request.session.get('post_step_one')
    step_two_data = request.session.get('post_step_two')
    step_three_data = request.session.get('post_step_three')
    pricing_type_data = request.session.get('pricing_data_type')

    if not step_one_data:
        return redirect("proposals:proposal_step_one")

    if not step_two_data:
        return redirect("proposals:proposal_step_two")
    
    if not step_three_data:
        return redirect("proposals:proposal_step_three")
    
    if pricing_type_data is None:
        return redirect("proposals:proposal_step_two")
    
    config_pricing = True if pricing_type_data else False

    if request.method == 'POST':
        proposalformfour = ProposalStepFourForm(request.POST, request.FILES)
        if proposalformfour.is_valid():
            # unpack and combine all form data from previous steps and current step
            with db_transaction.atomic():
                form_data = {**step_one_data, **step_two_data, **step_three_data, **proposalformfour.cleaned_data}
                # Create Post object
                team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id)
                form_data.pop('skill', None)
                category_id = form_data.pop('category', None)
                
                proposal = Proposal.objects.create(
                    pricing = config_pricing,
                    **form_data,
                    category_id=category_id,
                    created_by=request.user,
                    team=team,
                )
                
                proposal.skill.set(proposalformfour.cleaned_data['skill'])
                proposal.slug = slugify(proposal.title)
                proposal.save()

                del request.session['post_step_one']
                del request.session['post_step_two']
                del request.session['post_step_three']
                del request.session['pricing_data_type']

                return render(request, 'proposals/partials/create_steps.html', {'variable': 'stepFive', 'proposal':proposal})
        else:
            messages.error(request, 'Error occured in some steps.')
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

    proposalformtwo = ProposalStepTwoTierForm(request.POST or None, instance=proposal)
    if proposal.pricing == False:
        proposalformtwo = ProposalStepTwoSingleForm(request.POST or None, instance=proposal)
    
    if proposalformtwo.is_valid():
        proposalformtwo.pricing = proposal.pricing
        proposalformtwo.save()

        messages.info(request, 'Changed successfully.')

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
    proposal = Proposal.objects.select_related('category','team', 'created_by').filter(team=team, status = Proposal.ACTIVE)

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
    if request.merchant.proposal_detail == False:
        return render(request, 'proposals/proposal_detail.html', context)
    else:
        return render(request, 'proposals/proposal_detail2.html', context)


@login_required
@user_is_client
def product_detail(request, proposal_slug):
    proposal = get_object_or_404(Proposal, slug=proposal_slug, status=Proposal.ACTIVE)
    products = ProposalProduct.objects.filter(proposal=proposal, status=True).order_by('created_at')
    base_currency = get_base_currency_symbol()
    context = {
        "proposal": proposal,
        "products": products,
        'base_currency':base_currency,
    }
    
    return render(request, 'proposals/product_detail.html', context)


@login_required
@user_is_freelancer
def create_product_view(request, proposal_ref):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    proposal = get_object_or_404(Proposal, identifier=proposal_ref, team=team)
    products = ProposalProduct.objects.filter(proposal=proposal, team=team)
    productform = ProposalProductForm()
    base_currency = get_base_currency_symbol()
    context = {
        "proposal": proposal,
        "productform": productform,
        "products": products,
        'base_currency':base_currency,
    }
    
    return render(request, 'proposals/create_product.html', context)


@login_required
@user_is_client
def add_products(request, proposal_id):
    proposal = get_object_or_404(Proposal, pk=proposal_id, status=Proposal.ACTIVE)
    product_ids = request.GET.getlist('products[]')
    # product = get_object_or_404(ProposalProduct, proposal=proposal, pk=product_id, status=True)
    # print('product_id ::', product_ids)

    hiringbox = HiringBox(request)
    session = request.session
    selected_session = session.get('selected_product', {})
    print('BEFORE ::',selected_session)

    for product_id in product_ids:
        products = ProposalProduct.objects.filter(proposal=proposal, id=int(product_id)).first()
        # if products is not None and f'proposal_product' not in session:

        #     selected_session['proposal_product']['product_id'] = products.id
        #     selected_session['proposal_product']['price'] = products.price
        #     session.modified = True

        if products is not None:
            hiringbox.add_product(products)
            print(hiringbox.add_product(products))

    # selected_session = hiringbox.get_products()
    # products_price = hiringbox.get_products_price()
    # print('AFTER ::',selected_session)
    # print('TOTAL ::',products_price)

    
    # print('selected_product ::', selected_product)
    
    return JsonResponse({'totalprice':10})


@login_required
@user_is_freelancer
def add_product_attachment(request, proposal_id):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    proposal = get_object_or_404(Proposal, pk=proposal_id, team=team)
    
    if request.method == 'POST':
        productform = ProposalProductForm(request.POST or None, request.FILES or None)
        if productform.is_valid():
            product = productform.save(commit=False)
            product.proposal = proposal
            product.team=team
            product.created_by=request.user
            product.merchant=request.merchant
            product.save()

            if proposal.digital == False:
                proposal.digital = True
                proposal.save()

            context = {
                "proposal": proposal,
                "productform": productform,
                'product':product,
            }
            return render(request, 'proposals/partials/list_product.html', context)

    productform = ProposalProductForm()
    context = {
        "proposal": proposal,
        "productform": productform
    }
    
    return render(request, 'proposals/partials/create_product.html', context)


@login_required
@user_is_freelancer
def product_update(request, proposal_slug, product_id):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    proposal = get_object_or_404(Proposal, slug=proposal_slug, team=team)
    product = get_object_or_404(ProposalProduct, proposal=proposal, pk=product_id)
    
    if product.status == True:
        product.status = False
        product.save()
    else:
        product.status = True
        product.save()

    context = {
        'proposal':proposal,
        'product':product,
    }
    return render(request, 'proposals/partials/list_product.html', context)
    # return redirect('proposals:create_product_view', proposal_slug=proposal.slug)


@login_required
def product_download(request, proposal_slug, product_id):
    proposal = get_object_or_404(Proposal, slug=proposal_slug)
    product = get_object_or_404(ProposalProduct, proposal=proposal, pk=product_id)
    file = product.attachment.open(mode='rb')
    filename = product.attachment.name
    response = FileResponse(file)
    content_type, _ = mimetypes.guess_type(filename)
    response['Content-Type']  = content_type or 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename={product.attachment}'
    return response
    

def proposal_detail(request, short_name, proposal_slug):
    proposal = get_object_or_404(Proposal, created_by__short_name=short_name, slug=proposal_slug, status = Proposal.ACTIVE)
    profile_view = get_object_or_404(Freelancer, user=proposal.created_by)   
    other_proposals = Proposal.objects.exclude(pk=proposal.id)[:4]    
    team_members = proposal.team.members.all()

    # proposal_review_msg = ProposalReview.objects.filter(
    #     resolution__proposal_sale__proposal__team=proposal.team, 
    #     resolution__proposal_sale__proposal=proposal,
    #     status = True
    # )[:15]

    # review_status = (proposal_review_msg.count() < 1)

    # proposal_review_avg = proposal_review_average(proposal.team, proposal)
    # contract_review_avg = contract_review_average(proposal.team, proposal)

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
        # "proposal_review_avg": proposal_review_avg,
        # "contract_review_avg": contract_review_avg,
        # "proposal_review_msg":proposal_review_msg,
        # "review_status":review_status,
        "sesion_proposal":sesion_proposal,
        "all_viewed_proposals":all_viewed_proposals,
    }
    if request.merchant.proposal_detail == False:
        return render(request, 'proposals/proposal_detail.html', context)
    else:
        return render(request, 'proposals/proposal_detail2.html', context)


@login_required
def proposal_chat_messages(request, proposal_slug):
    proposal=None
    if request.user.user_type == Customer.FREELANCER:    
        team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user])
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
    return render(request, 'proposals/components/chat_messages.html', context)


@login_required
def fetch_messages(request, proposal_id):
    proposal = get_object_or_404(Proposal, pk=proposal_id)
    chats = ProposalChat.objects.filter(proposal=proposal, team=proposal.team)

    context = {
        'proposal':proposal,
        'chats':chats,
    }
    return render(request, 'proposals/components/chat_messages.html', context)

