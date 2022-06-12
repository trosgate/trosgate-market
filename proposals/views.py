import random
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proposal
from teams.models import Team
from django.contrib.auth.decorators import login_required
from .forms import ProposalStepOneForm, ProposalStepTwoForm, ProposalStepThreeForm, ProposalStepFourForm, ProposalCreationForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from freelancer.models import Freelancer
from account.permission import user_is_freelancer
from general_settings.models import Category, ProposalGuides
from datetime import datetime, timezone, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OfferContractForm
from .models import OfferContract
from teams.models import Team
from django.utils.text import slugify
from django.contrib import auth, messages
from django.views.decorators.cache import cache_control #prevent back button on browser after form submission


@login_required
@user_is_freelancer
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def proposal_step_one(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    session = request.session
    proposal = ''
    if "proposalstepone" not in session:
        proposalformone = ProposalStepOneForm(request.POST)

        if proposalformone.is_valid():
            proposal = proposalformone.save(commit=False)
            proposal.created_by = request.user
            proposal.team = team
            proposal.slug = slugify(proposal.title)
            proposal.save()
            proposalformone.save_m2m()

            session["proposalstepone"] = {"proposalstepone_id": proposal.id}
            session.modified = True

            return redirect("proposals:proposal_step_two")

    else:
        proposalstepone = Proposal.objects.get(pk=session["proposalstepone"]["proposalstepone_id"], team=team)
        proposalformone = ProposalStepOneForm(request.POST, instance = proposalstepone) 

        if proposalformone.is_valid():
            proposalformone.instance.title = proposalformone.cleaned_data['title']
            proposalformone.instance.preview = proposalformone.cleaned_data['preview']
            proposalformone.instance.category = proposalformone.cleaned_data['category']
            proposalformone.save()

 
            return redirect("proposals:proposal_step_two") 

        proposalformone = ProposalStepOneForm(instance = proposalstepone)           

    context = {
        'proposalformone': proposalformone,
    }
    return render(request, 'proposals/proposal_step_one.html', context)


@login_required
@user_is_freelancer
def proposal_step_two(request):

    if "proposalstepone" not in request.session:
        return redirect("proposals:proposal_step_one")

    proposal = ''                                                  
    proposalformtwo = ''           
    session = request.session

    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    proposalsteptwo = Proposal.objects.get(pk=session["proposalstepone"]["proposalstepone_id"], team=team)

    if "proposalsteptwo" not in session:
        proposalformtwo = ProposalStepTwoForm(request.POST, instance = proposalsteptwo)

        if proposalformtwo.is_valid():
            proposalformtwo.instance.description = proposalformtwo.cleaned_data['description']
            proposalformtwo.instance.sample_link = proposalformtwo.cleaned_data['sample_link']
            proposal = proposalformtwo.save()

            session["proposalsteptwo"] = {"proposalsteptwo_id": proposal.id}
            session.modified = True

            return redirect("proposals:proposal_step_three")

    else:
        proposalformtwo = ProposalStepTwoForm(request.POST, instance = proposalsteptwo)        
        if proposalformtwo.is_valid():
            description = proposalformtwo.cleaned_data['description']
            sample_link = proposalformtwo.cleaned_data['sample_link']

            Proposal.objects.filter(pk=session["proposalstepone"]["proposalstepone_id"], team=team).update(
                description=description, sample_link=sample_link)

            return redirect("proposals:proposal_step_three") 

        proposalformtwo = ProposalStepTwoForm(instance = proposalsteptwo)

    context = {
        'proposalformtwo': proposalformtwo,
    }
    return render(request, 'proposals/proposal_step_two.html', context)



@login_required
@user_is_freelancer
def proposal_step_three(request):
    proposal = ''                                       
    proposalstepthree = ''           
    proposalformthree = ''           
    session = request.session

    if "proposalstepone" not in request.session:
        return redirect("proposals:proposal_step_one")

    if "proposalsteptwo" not in request.session:
        return redirect("proposals:proposal_step_two")

    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)

    proposalstepthree = Proposal.objects.get(pk=session["proposalsteptwo"]["proposalsteptwo_id"], team=team)


    if "proposalstepthree" not in session:
        proposalformthree = ProposalStepThreeForm(request.POST, instance=proposalstepthree)

        if proposalformthree.is_valid():                        
            proposalformthree.instance.faq_one = proposalformthree.cleaned_data['faq_one']
            proposalformthree.instance.faq_one_description = proposalformthree.cleaned_data['faq_one_description']
            proposalformthree.instance.faq_two = proposalformthree.cleaned_data['faq_two']
            proposalformthree.instance.faq_two_description = proposalformthree.cleaned_data['faq_two_description']
            proposalformthree.instance.faq_three = proposalformthree.cleaned_data['faq_three']
            proposalformthree.instance.faq_three_description = proposalformthree.cleaned_data['faq_three_description']
            proposal = proposalformthree.save()

            session["proposalstepthree"] = {"proposalstepthree_id": proposal.id}
            session.modified = True

            return redirect("proposals:proposal_step_four")

    else:
        proposalformthree = ProposalStepThreeForm(request.POST, instance = proposalstepthree)

        if proposalformthree.is_valid():                        
            faq_one = proposalformthree.cleaned_data['faq_one']
            faq_one_description = proposalformthree.cleaned_data['faq_one_description']
            faq_two = proposalformthree.cleaned_data['faq_two']
            faq_two_description = proposalformthree.cleaned_data['faq_two_description']
            faq_three = proposalformthree.cleaned_data['faq_three']
            faq_three_description = proposalformthree.cleaned_data['faq_three_description']

            proposal = Proposal.objects.filter(pk=session["proposalsteptwo"]["proposalsteptwo_id"], team=team).update(
                faq_one=faq_one, faq_one_description=faq_one_description, 
                faq_two=faq_two, faq_two_description=faq_two_description,
                faq_three=faq_three, faq_three_description=faq_three_description
            )
            return redirect("proposals:proposal_step_four")  

        proposalformthree = ProposalStepThreeForm(instance = proposalstepthree)

    context = {
        'proposalformthree': proposalformthree,
    }
    return render(request, 'proposals/proposal_step_three.html', context)



@login_required
@user_is_freelancer
def proposal_step_four(request):                              
    proposalformfour = ''           
    session = request.session

    if "proposalstepone" not in request.session:
        return redirect("proposals:proposal_step_one")

    if "proposalsteptwo" not in request.session:
        return redirect("proposals:proposal_step_two")

    if "proposalstepthree" not in request.session:
        return redirect("proposals:proposal_step_three")

    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    proposalstepfour = Proposal.objects.get(pk=session["proposalstepthree"]["proposalstepthree_id"], team=team)   

    proposalformfour = ProposalStepFourForm(request.POST, request.FILES, instance = proposalstepfour)

    if proposalformfour.is_valid():
        proposalformfour.instance.salary = proposalformfour.cleaned_data['salary']
        proposalformfour.instance.service_level = proposalformfour.cleaned_data['service_level']
        proposalformfour.instance.revision = proposalformfour.cleaned_data['revision']
        proposalformfour.instance.dura_converter = proposalformfour.cleaned_data['dura_converter']
        proposalformfour.instance.thumbnail = proposalformfour.cleaned_data['thumbnail']
        proposalformfour.save()

        del session["proposalstepone"]
        del session["proposalsteptwo"]
        del session["proposalstepthree"]

        return redirect("proposals:review_proposal")

    else:
        proposalformfour = ProposalStepFourForm(instance = proposalstepfour)

    context = {      
        'proposalformfour': proposalformfour,
    }
    return render(request, 'proposals/proposal_step_four.html', context)



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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_proposal(request, short_name, proposal_slug):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)  
    proposal = get_object_or_404(Proposal, team=team, created_by__short_name=short_name,  slug=proposal_slug)

    if request.method == 'POST':
        proposalform = ProposalCreationForm(request.POST, request.FILES, instance=proposal)
        if proposalform.is_valid():
            proposalform.save()
            

            messages.success(request, 'The Changes were saved successfully!')

            return redirect('proposals:active_proposal')

    else:
        proposalform = ProposalCreationForm(instance=proposal)
    context = {
        "proposalform": proposalform,
        'proposals':proposal,
    }
    return render(request, 'proposals/update_proposal.html', context)


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
def modify_proposal_page(request, proposal_slug):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    Proposal.objects.filter(team=team, slug=proposal_slug).update(status = Proposal.MODIFY)


#this will appear in search result even without login
def proposal_list(request):
    category = Category.objects.filter(visible = True)
    proposals_list = Proposal.objects.filter(status = Proposal.ACTIVE)
    context = {
        "category":category, 
        "proposals_list": proposals_list,
    }
    return render(request, 'proposals/proposal_listing.html', context)


@login_required
@user_is_freelancer
def proposal_preview(request, short_name, proposal_slug):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    proposal = get_object_or_404(Proposal, slug=proposal_slug, created_by__short_name=short_name, team=team)
    profile_view = get_object_or_404(Freelancer, user=proposal.created_by)
    
    team_members = proposal.team.members.all()
    guides = ProposalGuides.objects.all()   
    
    
    context = {
        "proposal": proposal,
        "team_members": team_members,
        "profile_view": profile_view,
        "guides": guides,

    }
    return render(request, 'proposals/proposal_detail.html', context)



def proposal_detail(request, short_name, proposal_slug):
    proposal = get_object_or_404(Proposal, slug=proposal_slug, created_by__short_name=short_name, status = Proposal.ACTIVE, published=True)
    profile_view = get_object_or_404(Freelancer, user=proposal.created_by)
    
    team_members = proposal.team.members.all()
    guides = ProposalGuides.objects.all()

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
        "proposal": proposal,
        "team_members": team_members,
        "profile_view": profile_view,
        "guides": guides,
        "all_viewed_proposals":all_viewed_proposals,
    }
    return render(request, 'proposals/proposal_detail.html', context)



# def create_invoice_client(request):
#     team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
#     invoice_client = ClientInvoice.objects.filter(team=team)

#     if request.method == 'POST':
#         invoiceclientform = ClientInvoiceCreationForm(request.POST)
#         if invoiceclientform.is_valid():
#             invoiceclient = invoiceclientform.save(commit=False)
#             invoiceclient.created_by = request.user
#             invoiceclient.team = team
#             invoiceclient.save()

#             messages.success(request, 'The client was added successfully!')
#     else:
#         invoiceclientform = ClientInvoiceCreationForm()
#     context ={
#         'invoiceclientform':invoiceclientform,
#         'team':team,
#         'invoice_client':invoice_client,
#         'invoice_client':invoice_client,
#     }
#     return render (request, 'proposals/create_invoice_client.html', context )    
           

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_invoice(request):
    team = get_object_or_404(Team, pk=request.user.freelancer.active_team_id, members__in=[request.user], status=Team.ACTIVE)
    
    invoiceform = OfferContractForm(team, request.POST)
    # invoiceclientform = ClientInvoiceCreationForm(request.POST)

    # if request.method == 'POST' and invoiceclientform.is_valid():
    #         invoiceclient = invoiceclientform.save(commit=False)
    #         invoiceclient.created_by = request.user
    #         invoiceclient.team = team
    #         invoiceclient.save()
    
    if request.method == 'POST':
        if invoiceform.is_valid():
            new_invoice = invoiceform.save(commit=False)
            new_invoice.created_by = request.user
            new_invoice.team = team
            new_invoice.slug = slugify(new_invoice.client.name)
            new_invoice.save()

            messages.success(request, 'The invoice was created successfully!')

    else:
        invoiceform = OfferContractForm(team)
    context ={
        'invoiceform':invoiceform,
        # 'invoiceclientform':invoiceclientform,
        'team':team,
    }
    return render (request, 'proposals/create_invoice.html', context )            


#