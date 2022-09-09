from django.db.models import F
from . models import NewStats



class Middleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def stats(self, os_info):
        if "win" in os_info:
            NewStats.objects.all().update(win=F('win') + 1)
        elif "mac" in os_info:
            NewStats.objects.all().update(mac=F('mac') + 1)
        elif "iPhone" in os_info:
            NewStats.objects.all().update(iph=F('iph') + 1)
        elif "Android" in os_info:
            NewStats.objects.all().update(android=F('android') + 1)
        else:
            NewStats.objects.all().update(oth=F('oth') + 1)

 
    def __call__(self, request):
        response = self.get_response(request)

        if 'admin' not in request.path:
            self.stats(request.META['HTTP_USER_AGENT']) 

        return response

























