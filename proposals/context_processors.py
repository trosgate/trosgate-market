from general_settings.models import Category
from .models import Proposal



def categories(request):
    return {
        'categories': Category.objects.filter(visible=True)
    }

def published_proposal(request):
    return {
        'proposal_list': Proposal.objects.filter(status = Proposal.ACTIVE, published=True)[0:12]
    }
