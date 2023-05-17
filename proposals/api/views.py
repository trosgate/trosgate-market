from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from proposals.api.serializers import ProposalSerializer
from proposals.models import Proposal
from django.shortcuts import get_object_or_404
from proposals.api.utilities import get_object_or_404_response
from rest_framework import status


@api_view(['GET'])
def api_proposal_list(request):
    proposal = Proposal.objects.filter(status = Proposal.ACTIVE)
    data = {}
    if proposal.count() > 0:
        serializer = ProposalSerializer(proposal, many=True)
        return Response(serializer.data)
    data['response'] = 'No proposal to display'
    return Response(data=data)


@api_view(['GET'])
def api_proposal_detail(request, short_name, proposal_slug):
    try:
        proposal = Proposal.objects.get(slug=proposal_slug, created_by__short_name=short_name, status = Proposal.ACTIVE)
    except Proposal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProposalSerializer(proposal)
    return Response(serializer.data)


@api_view(['PUT'])
def api_proposal_update(request, proposal_id, proposal_slug):
    try:
        proposal = Proposal.objects.get(slug=proposal_slug, pk=proposal_id, status = Proposal.ACTIVE)
    except Proposal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProposalSerializer(proposal, data=request.data, partial=True)
    # data = {}
    # if request.method == 'PUT':
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
        # data['success'] = 'Update Successful'
        # return Response(data=data)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





















