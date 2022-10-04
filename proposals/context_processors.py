from .models import Proposal


def published_proposal(request):
    if Proposal.active.count():
        proposal_list = Proposal.active.filter(published=True)[0:12]
        return {'proposal_list': proposal_list}
    return {'proposal_list': None}
