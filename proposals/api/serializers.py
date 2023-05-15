from rest_framework import serializers
from proposals.models import Proposal



class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = [
            'title', 'preview', 'category','skill', 'description', 'sample_link',
            'salary', 'service_level', 'revision', 'dura_converter', 'thumbnail',
            'faq_one','faq_one_description','faq_two','faq_two_description',
        ]

    # methods:
        # merchant
        # team
        # created_by as author