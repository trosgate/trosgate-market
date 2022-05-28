from django.shortcuts import render, redirect
from .models import TermsAndConditions, Hiring, Freelancing, Sponsorship
from .forms import SponsorForm
from django.contrib import messages


def terms_and_conditions(request):
    termsandcond = TermsAndConditions.objects.filter(is_published = True)
    return render(request, "pages/terms_and_conditions.html", {"termsandcond":termsandcond})


def how_it_works(request):
    hiring = Hiring.objects.filter(is_published = True)
    freelancing = Freelancing.objects.filter(is_published = True)
    sponsorship = Sponsorship.objects.filter(is_published = True)[:1]
    if request.method == 'POST':      

        sponsorform = SponsorForm(request.POST)

        if sponsorform.is_valid():
            sponsor = sponsorform.save(commit=False)
            sponsor.save()

            messages.info(request, f'Hello {sponsor.name}, your message was received. We shall get back')

            return redirect('pages:how_it_works')
    else:
        sponsorform = SponsorForm()
    context ={
        "hiring":hiring, 
        'freelancing':freelancing, 
        'sponsorship':sponsorship, 
        'sponsorform':sponsorform
    }
    return render(request, "pages/howitworks.html", context)