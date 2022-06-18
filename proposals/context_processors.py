from .models import Proposal


def published_proposal(request):
    return {
        'proposal_list': Proposal.objects.filter(status = Proposal.ACTIVE, published=True)[0:12]
    }
