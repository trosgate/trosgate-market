from django.http import HttpResponse
from .models import Customer
from teams.models import Team


def verify_username(request):
    short_name = request.POST.get('short_name')
    if len(short_name) < 4:
        return HttpResponse("<div style='color:red;'> The username must be four characters or more </div>")
    else:
        if Customer.objects.filter(short_name=short_name).exists():
            return HttpResponse("<div id='short_name-status' class='shortnameerrors'> Username already taken </div>")
        else:
            return HttpResponse("<div id='short_name-status' class='shortnamesuccess'> This username is available </div>") 


def verify_team(request):
    title = request.POST.get('title')
    if Team.objects.filter(title=title).exists():
        return HttpResponse("<div style='color:red;'> This name already taken </div>")
    else:
        return HttpResponse("<div style='color:green;'> This name is available </div>") 


def user_types(request):
    type = request.GET.get('user_type')
    if type =="freelancer":
        return HttpResponse("<div style='color:blue;'>Info: A freelancer will work and get paid</div>")
    else:
        return HttpResponse("<div style='color:blue;'>Info: A client will create jobs and employ</div>")
