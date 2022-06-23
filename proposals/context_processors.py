from .models import Proposal


def published_proposal(request):
    return {
        'proposal_list': Proposal.active.filter(published=True)[0:12]
    }
